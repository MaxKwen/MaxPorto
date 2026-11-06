(() => {
  const page = document.getElementById("achievement-page");
  if (!page) return;

  const copy = JSON.parse(document.getElementById("achievement-copy").textContent);
  const cardTemplate = document.getElementById("achievement-card-template");
  const grid = document.getElementById("achievement-grid");
  const searchForm = document.getElementById("achievement-search-form");
  const searchInput = document.getElementById("achievement-search-input");
  const retryButton = document.getElementById("achievement-retry");
  const emptyState = document.getElementById("achievement-empty");
  const states = {
    loading: document.getElementById("achievement-loading"),
    error: document.getElementById("achievement-error"),
    empty: emptyState,
    grid,
  };
  const SEARCH_DEBOUNCE_DELAY = 300;
  // Field yang dikirim ke serializer; token CSRF form tidak ikut sebagai data
  const TEXT_FIELDS = ["title", "title_id", "result", "result_id", "category"];
  // year boleh null; display_order dihilangkan bila kosong agar default model (0) dipakai
  const NULLABLE_NUMBER_FIELDS = ["year"];
  const OPTIONAL_NUMBER_FIELDS = ["display_order"];
  const achievementsById = new Map();
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

  function localizedValue(achievement, name) {
    return copy.language === "id" && achievement[`${name}_id`]
      ? achievement[`${name}_id`]
      : achievement[name];
  }

  function buildAchievementCard(achievement) {
    const card = cardTemplate.content.firstElementChild.cloneNode(true);
    const title = localizedValue(achievement, "title");
    card.dataset.id = achievement.id;

    // Teks dari pengguna selalu lewat textContent, tidak pernah lewat innerHTML
    card.querySelector("h2").textContent = title;
    card.querySelector(".achievement-category").textContent = achievement.category;
    const year = card.querySelector(".achievement-year");
    if (achievement.year != null) year.textContent = achievement.year;
    else year.remove();
    card.querySelector(".achievement-result").textContent =
      localizedValue(achievement, "result");

    const editButton = card.querySelector(".achievement-edit");
    if (editButton) editButton.setAttribute("aria-label", `${copy.edit_achievement}: ${title}`);
    const deleteButton = card.querySelector(".achievement-delete");
    if (deleteButton) deleteButton.setAttribute("aria-label", `${copy.delete_achievement}: ${title}`);

    const star = card.querySelector(".button-star");
    star.classList.toggle("is-starred", achievement.is_starred);
    star.title = achievement.star_count > 0
      ? `${copy.starred_by} ${achievement.starred_by_names}`
      : copy.first_star;
    if (star.classList.contains("achievement-star")) {
      star.querySelector(".star-label").textContent = achievement.is_starred ? copy.unstar : copy.star;
    }
    star.querySelector(".star-count").textContent = achievement.star_count;
    return card;
  }

  async function fetchAchievements(query = "") {
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
      if (!Array.isArray(items)) throw new Error("Invalid achievement response");
      if (controller.signal.aborted || controller !== activeController) return;

      achievementsById.clear();
      items.forEach((item) => achievementsById.set(String(item.id), item));
      if (items.length === 0) {
        grid.replaceChildren();
        emptyState.querySelector("p").textContent = query ? copy.no_results : copy.empty_state;
        showState("empty");
        return;
      }
      grid.replaceChildren(...items.map(buildAchievementCard));
      showState("grid");
    } catch (error) {
      if (error.name === "AbortError" || controller !== activeController) return;
      console.error("Error loading achievement:", error);
      showState("error");
    }
  }

  function refreshList() {
    clearTimeout(searchTimer);
    return fetchAchievements(searchInput.value.trim());
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

  const formModal = document.getElementById("achievement-form-modal");
  const achievementForm = document.getElementById("achievement-form");
  const formTitle = document.getElementById("achievement-form-title");
  const addButton = document.getElementById("achievement-add-button");
  const submitButton = achievementForm?.querySelector('button[type="submit"]');
  let editingId = null;
  let saving = false;

  function clearFormErrors() {
    achievementForm.querySelectorAll("[data-error-for]").forEach((element) => {
      element.textContent = "";
    });
    achievementForm.querySelectorAll("[aria-invalid]").forEach((field) => {
      field.removeAttribute("aria-invalid");
    });
    const summary = document.getElementById("achievement-form-errors");
    summary.textContent = "";
    summary.classList.add("hide");
  }

  // Tampilkan error per field dari serializer di bawah input masing-masing
  function displayFormErrors(errors) {
    Object.entries(errors || {}).forEach(([name, fieldErrors]) => {
      const text = [].concat(fieldErrors).join(" ");
      const field = achievementForm.elements.namedItem(name);
      const errorElement = achievementForm.querySelector(`[data-error-for="${CSS.escape(name)}"]`);
      if (field && errorElement) {
        field.setAttribute("aria-invalid", "true");
        errorElement.textContent = text;
      } else {
        const summary = document.getElementById("achievement-form-errors");
        summary.textContent = text;
        summary.classList.remove("hide");
      }
    });
  }

  function setMode(achievement) {
    editingId = achievement ? String(achievement.id) : null;
    clearFormErrors();
    achievementForm.reset();
    if (achievement) {
      [...TEXT_FIELDS, ...NULLABLE_NUMBER_FIELDS, ...OPTIONAL_NUMBER_FIELDS].forEach((name) => {
        const field = achievementForm.elements.namedItem(name);
        if (field) field.value = achievement[name] ?? "";
      });
    }
    formTitle.textContent = achievement ? copy.edit_heading : copy.add_heading;
    submitButton.textContent = achievement ? copy.save_changes : copy.add_achievement;
  }

  function formPayload() {
    const fields = new FormData(achievementForm);
    const payload = {};
    TEXT_FIELDS.forEach((name) => { payload[name] = fields.get(name) ?? ""; });
    NULLABLE_NUMBER_FIELDS.forEach((name) => {
      const value = String(fields.get(name) ?? "").trim();
      payload[name] = value === "" ? null : Number(value);
    });
    OPTIONAL_NUMBER_FIELDS.forEach((name) => {
      const value = String(fields.get(name) ?? "").trim();
      if (value !== "") payload[name] = Number(value);
    });
    return payload;
  }

  async function saveAchievement(event) {
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
        submitButton.textContent = editingId !== null ? copy.save_changes : copy.add_achievement;
      }
    }
  }

  if (achievementForm && formModal) {
    achievementForm.addEventListener("submit", saveAchievement);
    // Tombol tambah membuka modal yang sama dalam mode tambah
    if (addButton) addButton.addEventListener("click", () => setMode(null));
  }

  // ---------- Hapus (DELETE) dengan modal konfirmasi ----------

  const deleteModal = document.getElementById("achievement-delete-modal");
  const deleteConfirm = document.getElementById("achievement-delete-confirm");
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
    const card = button?.closest(".achievement-card");
    if (!button || !card || button.disabled) return;
    const achievement = achievementsById.get(card.dataset.id);
    if (!achievement) return;

    if (button.classList.contains("achievement-edit") && formModal) {
      setMode(achievement);
      formModal.showPopover();
    } else if (button.classList.contains("achievement-delete") && deleteModal) {
      deletingId = String(achievement.id);
      document.getElementById("achievement-delete-name").textContent =
        localizedValue(achievement, "title");
      deleteModal.showPopover();
    } else if (button.classList.contains("achievement-star")) {
      // Toggle: tombol dikunci selama request agar tidak terkirim dua kali
      button.disabled = true;
      try {
        const updated = await sendJson(endpointFor(page.dataset.starEndpoint, achievement.id), "POST");
        achievementsById.set(String(updated.id), updated);
        card.replaceWith(buildAchievementCard(updated));
      } catch (error) {
        showToast(copy.star_error_title, error.message, "error");
        button.disabled = false;
      }
    }
  });

  refreshList();
})();
