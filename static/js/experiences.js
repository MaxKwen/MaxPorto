(() => {
  const page = document.getElementById("experience-page");
  if (!page) return;

  const copy = JSON.parse(document.getElementById("experience-copy").textContent);
  const cardTemplate = document.getElementById("experience-card-template");
  const grid = document.getElementById("experience-grid");
  const searchForm = document.getElementById("experience-search-form");
  const searchInput = document.getElementById("experience-search-input");
  const retryButton = document.getElementById("experience-retry");
  const emptyState = document.getElementById("experience-empty");
  const states = {
    loading: document.getElementById("experience-loading"),
    error: document.getElementById("experience-error"),
    empty: emptyState,
    grid,
  };
  const SEARCH_DEBOUNCE_DELAY = 300;
  // Field yang dikirim ke serializer; token CSRF form tidak ikut sebagai data
  const TEXT_FIELDS = [
    "title", "title_id", "organization", "organization_id",
    "description", "description_id", "category",
  ];
  const YEAR_FIELDS = ["start_year", "end_year"];
  const experiencesById = new Map();
  let searchTimer;
  let activeController;

  // ---------- Helper request API (CSRF + JSON + pesan error DRF) ----------

  function getCookie(name) {
    const prefix = `${name}=`;
    const cookie = document.cookie.split(";").map((value) => value.trim())
      .find((value) => value.startsWith(prefix));
    return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
  }

  function endpointFor(pattern, id) {
    return pattern.replace("/0/", `/${encodeURIComponent(id)}/`);
  }

  class ApiError extends Error {
    constructor(message, status, data) {
      super(message);
      this.status = status;
      this.data = data;
    }
  }

  // Error DRF: {"field": ["..."]}, {"non_field_errors": [...]}, atau {"detail": "..."}
  function apiErrorMessage(data, status) {
    const messages = Object.values(data || {}).flat().filter((value) => typeof value === "string");
    if (messages.length) return messages.join(" ");
    return status === 403 ? copy.request_rejected : copy.add_error;
  }

  async function sendJson(url, method, payload) {
    let response;
    try {
      response = await fetch(url, {
        method,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: payload === undefined ? undefined : JSON.stringify(payload),
      });
    } catch (error) {
      throw new ApiError(copy.connection_error, 0, null);
    }
    if (response.status === 204) return null;
    const data = await response.json().catch(() => null);
    if (!response.ok) throw new ApiError(apiErrorMessage(data, response.status), response.status, data);
    return data;
  }

  // ---------- Daftar, pencarian, dan kartu ----------

  function showState(name) {
    Object.entries(states).forEach(([key, element]) => {
      element.classList.toggle("hide", key !== name);
    });
    grid.setAttribute("aria-busy", String(name === "loading"));
  }

  function localizedValue(experience, name) {
    return copy.language === "id" && experience[`${name}_id`]
      ? experience[`${name}_id`]
      : experience[name];
  }

  function buildExperienceCard(experience) {
    const card = cardTemplate.content.firstElementChild.cloneNode(true);
    const title = localizedValue(experience, "title");
    card.dataset.id = experience.id;

    // Teks dari pengguna selalu lewat textContent, tidak pernah lewat innerHTML
    card.querySelector("h2").textContent = title;
    card.querySelector(".experience-period").textContent =
      `${experience.start_year} — ${experience.end_year ?? copy.present}`;
    card.querySelector(".experience-category").textContent = experience.category;
    card.querySelector(".experience-organization").textContent =
      localizedValue(experience, "organization");
    card.querySelector(".experience-description").textContent =
      localizedValue(experience, "description");

    const editButton = card.querySelector(".experience-edit");
    if (editButton) editButton.setAttribute("aria-label", `${copy.edit_experience}: ${title}`);
    const deleteButton = card.querySelector(".experience-delete");
    if (deleteButton) deleteButton.setAttribute("aria-label", `${copy.delete_experience}: ${title}`);

    const star = card.querySelector(".button-star");
    star.classList.toggle("is-starred", experience.is_starred);
    star.title = experience.star_count > 0
      ? `${copy.starred_by} ${experience.starred_by_names}`
      : copy.first_star;
    if (star.classList.contains("experience-star")) {
      star.querySelector(".star-label").textContent = experience.is_starred ? copy.unstar : copy.star;
    }
    star.querySelector(".star-count").textContent = experience.star_count;
    return card;
  }

  async function fetchExperiences(query = "") {
    if (activeController) activeController.abort();
    const controller = new AbortController();
    activeController = controller;
    showState("loading");

    try {
      const url = new URL(page.dataset.endpoint, window.location.origin);
      if (query) url.searchParams.set("q", query);
      const response = await fetch(url, {
        headers: { Accept: "application/json" },
        signal: controller.signal,
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const items = await response.json();
      if (!Array.isArray(items)) throw new Error("Invalid experience response");
      if (controller.signal.aborted || controller !== activeController) return;

      experiencesById.clear();
      items.forEach((item) => experiencesById.set(String(item.id), item));
      if (items.length === 0) {
        grid.replaceChildren();
        emptyState.querySelector("p").textContent = query ? copy.no_results : copy.empty_state;
        showState("empty");
        return;
      }
      grid.replaceChildren(...items.map(buildExperienceCard));
      showState("grid");
    } catch (error) {
      if (error.name === "AbortError" || controller !== activeController) return;
      console.error("Error loading experience:", error);
      showState("error");
    }
  }

  function refreshList() {
    clearTimeout(searchTimer);
    return fetchExperiences(searchInput.value.trim());
  }

  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    // Batalkan hasil lama begitu kata kunci berubah
    if (activeController) activeController.abort();
    searchTimer = setTimeout(refreshList, SEARCH_DEBOUNCE_DELAY);
  });
  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    refreshList();
  });
  retryButton.addEventListener("click", refreshList);

  // ---------- Modal tambah (POST) dan edit (PATCH) ----------

  const formModal = document.getElementById("experience-form-modal");
  const experienceForm = document.getElementById("experience-form");
  const formTitle = document.getElementById("experience-form-title");
  const addButton = document.getElementById("experience-add-button");
  const submitButton = experienceForm?.querySelector('button[type="submit"]');
  let editingId = null;
  let saving = false;

  function clearFormErrors() {
    experienceForm.querySelectorAll("[data-error-for]").forEach((element) => {
      element.textContent = "";
    });
    experienceForm.querySelectorAll("[aria-invalid]").forEach((field) => {
      field.removeAttribute("aria-invalid");
    });
    const summary = document.getElementById("experience-form-errors");
    summary.textContent = "";
    summary.classList.add("hide");
  }

  // Tampilkan error per field dari serializer di bawah input masing-masing
  function displayFormErrors(errors) {
    Object.entries(errors || {}).forEach(([name, fieldErrors]) => {
      const text = [].concat(fieldErrors).join(" ");
      const field = experienceForm.elements.namedItem(name);
      const errorElement = experienceForm.querySelector(`[data-error-for="${CSS.escape(name)}"]`);
      if (field && errorElement) {
        field.setAttribute("aria-invalid", "true");
        errorElement.textContent = text;
      } else {
        const summary = document.getElementById("experience-form-errors");
        summary.textContent = text;
        summary.classList.remove("hide");
      }
    });
  }

  function setMode(experience) {
    editingId = experience ? String(experience.id) : null;
    clearFormErrors();
    experienceForm.reset();
    if (experience) {
      [...TEXT_FIELDS, ...YEAR_FIELDS].forEach((name) => {
        const field = experienceForm.elements.namedItem(name);
        if (field) field.value = experience[name] ?? "";
      });
    }
    formTitle.textContent = experience ? copy.edit_heading : copy.add_heading;
    submitButton.textContent = experience ? copy.save_changes : copy.add_experience;
  }

  function formPayload() {
    const fields = new FormData(experienceForm);
    const payload = {};
    TEXT_FIELDS.forEach((name) => { payload[name] = fields.get(name) ?? ""; });
    YEAR_FIELDS.forEach((name) => {
      const value = String(fields.get(name) ?? "").trim();
      payload[name] = value === "" ? null : Number(value);
    });
    return payload;
  }

  async function saveExperience(event) {
    event.preventDefault();
    if (saving) return;
    saving = true;
    clearFormErrors();
    const isEdit = editingId !== null;
    submitButton.disabled = true;
    submitButton.textContent = isEdit ? copy.saving : copy.adding;

    try {
      if (isEdit) {
        await sendJson(endpointFor(page.dataset.detailEndpoint, editingId), "PATCH", formPayload());
      } else {
        await sendJson(page.dataset.endpoint, "POST", formPayload());
      }
      formModal.hidePopover();
      showToast(copy.add_success_title, isEdit ? copy.edit_success : copy.add_success, "success");
      setMode(null);
      await refreshList();
    } catch (error) {
      // 400: error per field tetap terlihat di modal; 403/jaringan: cukup toast
      if (error.status === 400) displayFormErrors(error.data);
      showToast(isEdit ? copy.edit_error_title : copy.add_error_title, error.message, "error");
    } finally {
      saving = false;
      submitButton.disabled = false;
      if (submitButton.textContent === copy.saving || submitButton.textContent === copy.adding) {
        submitButton.textContent = editingId !== null ? copy.save_changes : copy.add_experience;
      }
    }
  }

  if (experienceForm && formModal) {
    experienceForm.addEventListener("submit", saveExperience);
    // Tombol tambah membuka modal yang sama dalam mode tambah
    if (addButton) addButton.addEventListener("click", () => setMode(null));
  }

  // ---------- Hapus (DELETE) dengan modal konfirmasi ----------

  const deleteModal = document.getElementById("experience-delete-modal");
  const deleteConfirm = document.getElementById("experience-delete-confirm");
  let deletingId = null;

  if (deleteModal && deleteConfirm) {
    deleteConfirm.addEventListener("click", async () => {
      if (deletingId === null || deleteConfirm.disabled) return;
      deleteConfirm.disabled = true;
      try {
        await sendJson(endpointFor(page.dataset.detailEndpoint, deletingId), "DELETE");
        deleteModal.hidePopover();
        showToast(copy.add_success_title, copy.delete_success, "success");
        await refreshList();
      } catch (error) {
        showToast(copy.delete_error_title, error.message, "error");
      } finally {
        deleteConfirm.disabled = false;
        deletingId = null;
      }
    });
  }

  // ---------- Event delegation untuk tombol di kartu ----------

  grid.addEventListener("click", async (event) => {
    const button = event.target.closest("button");
    const card = button?.closest(".experience-card");
    if (!button || !card || button.disabled) return;
    const experience = experiencesById.get(card.dataset.id);
    if (!experience) return;

    if (button.classList.contains("experience-edit") && formModal) {
      setMode(experience);
      formModal.showPopover();
    } else if (button.classList.contains("experience-delete") && deleteModal) {
      deletingId = String(experience.id);
      document.getElementById("experience-delete-name").textContent =
        localizedValue(experience, "title");
      deleteModal.showPopover();
    } else if (button.classList.contains("experience-star")) {
      // Toggle: tombol dikunci selama request agar tidak terkirim dua kali
      button.disabled = true;
      try {
        const updated = await sendJson(endpointFor(page.dataset.starEndpoint, experience.id), "POST");
        experiencesById.set(String(updated.id), updated);
        card.replaceWith(buildExperienceCard(updated));
      } catch (error) {
        showToast(copy.star_error_title, error.message, "error");
        button.disabled = false;
      }
    }
  });

  refreshList();
})();
