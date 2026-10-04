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
  let searchTimer;
  let activeController;
  let addingAchievement = false;

  function showState(name) {
    Object.entries(states).forEach(([key, element]) => {
      element.classList.toggle("hide", key !== name);
    });
    grid.setAttribute("aria-busy", String(name === "loading"));
  }

  function localizedValue(fields, name) {
    return copy.language === "id" && fields[`${name}_id`]
      ? fields[`${name}_id`]
      : fields[name];
  }

  function buildAchievementCard(item) {
    const achievement = item.fields;
    const card = cardTemplate.content.firstElementChild.cloneNode(true);
    const title = localizedValue(achievement, "title");

    // Keep user-supplied text out of HTML parsing, including labels and tooltips.
    card.querySelector("h2").textContent = title;
    card.querySelector(".achievement-category").textContent = achievement.category;
    const year = card.querySelector(".achievement-year");
    if (achievement.year != null) year.textContent = achievement.year;
    else year.remove();
    card.querySelector(".achievement-result").textContent =
      localizedValue(achievement, "result");

    const editLink = card.querySelector(".achievement-edit");
    if (editLink) {
      if (achievement.can_update) editLink.href = achievement.update_url;
      else editLink.remove();
    }

    const deleteButton = card.querySelector(".achievement-delete");
    const deleteModal = card.querySelector(".project-delete-modal");
    if (deleteButton && deleteModal) {
      if (achievement.can_delete) {
        const modalId = `delete-achievement-${item.pk}`;
        deleteModal.id = modalId;
        const heading = deleteModal.querySelector("h2");
        heading.id = `${modalId}-title`;
        deleteModal.setAttribute("aria-labelledby", heading.id);
        deleteModal.querySelector("strong").textContent = title;
        deleteModal.querySelector("form").action = achievement.delete_url;
        deleteModal.querySelectorAll("[popovertargetaction]").forEach((button) => {
          button.setAttribute("popovertarget", modalId);
        });
        deleteButton.setAttribute("popovertarget", modalId);
        deleteButton.setAttribute("aria-label", `${copy.delete_achievement}: ${title}`);
      } else {
        deleteButton.remove();
        deleteModal.remove();
      }
    }

    const starForm = card.querySelector(".star-form");
    const starButton = starForm.querySelector("button");
    starForm.action = achievement.star_url;
    starButton.classList.toggle("is-starred", achievement.is_starred);
    starButton.title = achievement.star_count > 0
      ? `${copy.starred_by} ${achievement.starred_by_names}`
      : copy.first_star;
    starButton.querySelector(".star-label").textContent =
      achievement.is_starred ? copy.unstar : copy.star;
    starButton.querySelector(".star-count").textContent = achievement.star_count;
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

      if (items.length === 0) {
        grid.replaceChildren();
        emptyState.querySelector("p").textContent = query
          ? copy.no_results
          : copy.empty_state;
        showState("empty");
        return;
      }

      const cards = items.map(buildAchievementCard);
      grid.replaceChildren(...cards);
      showState("grid");
    } catch (error) {
      if (error.name === "AbortError" || controller !== activeController) return;
      console.error("Error loading achievements:", error);
      showState("error");
    }
  }

  function searchAchievements() {
    clearTimeout(searchTimer);
    fetchAchievements(searchInput.value.trim());
  }

  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    // Invalidate an in-flight result as soon as the query changes.
    if (activeController) activeController.abort();
    searchTimer = setTimeout(searchAchievements, SEARCH_DEBOUNCE_DELAY);
  });
  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    searchAchievements();
  });
  retryButton.addEventListener("click", searchAchievements);
  const achievementForm = document.getElementById("achievement-form");
  const addModal = document.getElementById("add-achievement-modal");

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

  function displayFormErrors(errors) {
    const messages = [];
    Object.entries(errors).forEach(([name, fieldErrors]) => {
      const text = fieldErrors.map((error) => error.message).join(" ");
      const field = achievementForm.elements.namedItem(name);
      const errorElement = Array.from(
        achievementForm.querySelectorAll("[data-error-for]")
      ).find((element) => element.dataset.errorFor === name);
      if (field && errorElement) {
        field.setAttribute("aria-invalid", "true");
        errorElement.textContent = text;
        messages.push(`${field.labels[0].textContent}: ${text}`);
      } else {
        const summary = document.getElementById("achievement-form-errors");
        summary.textContent = text;
        summary.classList.remove("hide");
        messages.push(text);
      }
    });
    return messages.join(" ");
  }

  async function addAchievement(event) {
    event.preventDefault();
    if (addingAchievement) return;

    addingAchievement = true;
    clearFormErrors();
    const submitButton = achievementForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    submitButton.textContent = copy.adding;

    try {
      // FormData includes the CSRF token rendered by Django in the modal.
      const response = await fetch(achievementForm.action, {
        method: "POST",
        body: new FormData(achievementForm),
        headers: { Accept: "application/json" },
      });
      const result = await response.json().catch(() => null);

      if (response.status === 201 && result) {
        achievementForm.reset();
        addModal.hidePopover();
        showToast(copy.add_success_title, result.message || copy.add_success, "success");
        clearTimeout(searchTimer);
        await fetchAchievements(searchInput.value.trim());
      } else {
        const message = result?.errors
          ? displayFormErrors(result.errors)
          : (result?.message || (response.status === 403 ? copy.request_rejected : copy.add_error));
        showToast(copy.add_error_title, message || copy.add_error, "error");
      }
    } catch (error) {
      console.error("Error adding achievement:", error);
      showToast(copy.add_error_title, copy.connection_error, "error");
    } finally {
      addingAchievement = false;
      submitButton.disabled = false;
      submitButton.textContent = copy.add_achievement;
    }
  }

  // The modal is deliberately absent for guests, ordinary users, and Editors.
  if (achievementForm && addModal) {
    achievementForm.addEventListener("submit", addAchievement);
  }
  searchAchievements();
})();
