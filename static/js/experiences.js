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
  let searchTimer;
  let activeController;

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

  function buildExperienceCard(item) {
    const experience = item.fields;
    const card = cardTemplate.content.firstElementChild.cloneNode(true);
    const title = localizedValue(experience, "title");

    // Keep user-supplied text out of HTML parsing, including labels and tooltips.
    card.querySelector("h2").textContent = title;
    card.querySelector(".experience-period").textContent =
      `${experience.start_year} — ${experience.end_year ?? copy.present}`;
    card.querySelector(".experience-category").textContent = experience.category;
    card.querySelector(".experience-organization").textContent =
      localizedValue(experience, "organization");
    card.querySelector(".experience-description").textContent =
      localizedValue(experience, "description");

    const editLink = card.querySelector(".experience-edit");
    if (editLink) {
      if (experience.can_update) editLink.href = experience.update_url;
      else editLink.remove();
    }

    const deleteButton = card.querySelector(".experience-delete");
    const deleteModal = card.querySelector(".project-delete-modal");
    if (deleteButton && deleteModal) {
      if (experience.can_delete) {
        const modalId = `delete-experience-${item.pk}`;
        deleteModal.id = modalId;
        const heading = deleteModal.querySelector("h2");
        heading.id = `${modalId}-title`;
        deleteModal.setAttribute("aria-labelledby", heading.id);
        deleteModal.querySelector("strong").textContent = title;
        deleteModal.querySelector("form").action = experience.delete_url;
        deleteModal.querySelectorAll("[popovertargetaction]").forEach((button) => {
          button.setAttribute("popovertarget", modalId);
        });
        deleteButton.setAttribute("popovertarget", modalId);
        deleteButton.setAttribute("aria-label", `${copy.delete_experience}: ${title}`);
      } else {
        deleteButton.remove();
        deleteModal.remove();
      }
    }

    const starForm = card.querySelector(".star-form");
    const starButton = starForm.querySelector("button");
    starForm.action = experience.star_url;
    starButton.classList.toggle("is-starred", experience.is_starred);
    starButton.title = experience.star_count > 0
      ? `${copy.starred_by} ${experience.starred_by_names}`
      : copy.first_star;
    starButton.querySelector(".star-label").textContent =
      experience.is_starred ? copy.unstar : copy.star;
    starButton.querySelector(".star-count").textContent = experience.star_count;
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
      if (controller !== activeController) return;

      if (items.length === 0) {
        grid.replaceChildren();
        emptyState.querySelector("p").textContent = query
          ? copy.no_results
          : copy.empty_state;
        showState("empty");
        return;
      }

      const cards = items.map(buildExperienceCard);
      grid.replaceChildren(...cards);
      showState("grid");
    } catch (error) {
      if (error.name === "AbortError" || controller !== activeController) return;
      console.error("Error loading experience:", error);
      showState("error");
    }
  }

  function searchExperiences() {
    clearTimeout(searchTimer);
    fetchExperiences(searchInput.value.trim());
  }

  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    // Invalidate an in-flight result as soon as the query changes.
    if (activeController) activeController.abort();
    searchTimer = setTimeout(searchExperiences, SEARCH_DEBOUNCE_DELAY);
  });
  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    searchExperiences();
  });
  retryButton.addEventListener("click", searchExperiences);
  searchExperiences();
})();
