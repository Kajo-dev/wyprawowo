const createPostButton = document.querySelector(".inspire-us-button");
const createButtonModal = document.querySelector(".create-post");
const closeModalButton = document.querySelector(".btn-cancel");
const overlay = document.querySelector(".overlay");
const assetsField = document.querySelector(".photo_input");
const videosField = document.querySelector(".video-input");
const imagesBlock = document.querySelector(".images-block");
const videoBlock = document.querySelector(".videos-block");
const moreDaysCheckbox = document.querySelector("#longer_then_one_day");
const moreDaysLabel = document.querySelector(".end_date_label");
const moreDaysInput = document.querySelector("#date_end");
const eventFields = document.querySelectorAll("#event-fields .required-field");
const textFields = document.querySelectorAll("#text-fields .required-field");

function toggleModal(open) {
  if (open) {
    createButtonModal.classList.add("open");
  } else {
    createButtonModal.classList.remove("open");
  }
}

function toggleElementDisplay(element, displayStyle) {
  element.style.display = displayStyle;
}

function handlePostTypeChange(event) {
  const isEvent = event.target.value === "event";
  handleRequiredFields(event.target.value);
  toggleElementDisplay(
    document.getElementById("event-fields"),
    isEvent ? "grid" : "none"
  );
  toggleElementDisplay(
    document.getElementById("text-fields"),
    isEvent ? "none" : "block"
  );
}

function initializePostTypeDisplay() {
  const postTypeSelect = document.querySelector('select[name="post_type"]');
  handlePostTypeChange({ target: postTypeSelect });
}

function toggleCommentsSection(event) {
  const postId = event.target.getAttribute("data-post-id");
  const commentsSection = document.getElementById(
    "comments-section-wrapper-" + postId
  );
  const isHidden =
    commentsSection.style.display === "none" ||
    commentsSection.style.display === "";
  toggleElementDisplay(commentsSection, isHidden ? "block" : "none");
}

function handleFileChange(event) {
  const files = event.target.files;
  if (files.length === 0) return;

  const _document = document.createDocumentFragment();
  const isVideo = files[0].type === "video/mp4";
  const block = isVideo ? videoBlock : imagesBlock;

  block.innerHTML = "";

  [...files].forEach((file) => {
    const reader = new FileReader();
    const assetElement = isVideo
      ? document.createElement("video")
      : document.createElement("img");

    _document.appendChild(assetElement);

    reader.onload = function (e) {
      assetElement.src = e.target.result;
    };

    reader.readAsDataURL(file);

    assetElement.addEventListener("click", (event) => {
      event.stopPropagation();
      assetElement.classList.toggle("open");
    });
  });

  block.appendChild(_document);
}

function initializeEventListeners() {
  if (window.location.pathname === "/") {
    document
      .querySelector('select[name="post_type"]')
      .addEventListener("change", handlePostTypeChange);

    createPostButton.addEventListener("click", () => toggleModal(true));
    closeModalButton.addEventListener("click", (e) => {
      e.preventDefault();
      toggleModal(false);
    });

    overlay.addEventListener("click", (e) => {
      if (e.target.classList.contains("overlay")) {
        toggleModal(false);
      }
    });
  }

  document.querySelectorAll(".comment-counter").forEach((counter) => {
    counter.addEventListener("click", toggleCommentsSection);
  });
  if (window.location.pathname === "/") {
    [assetsField, videosField].forEach((el) => {
      el.addEventListener("change", handleFileChange);
    });
  }
}

const handleRequiredFields = (postType) => {
  if (postType === "event") {
    eventFields.forEach((field) => {
      field.setAttribute("required", true);
    });

    if (moreDaysInput.classList.contains("active")) {
      moreDaysInput.setAttribute("required", true);
    }

    textFields.forEach((field) => {
      field.removeAttribute("required");
    });
  } else if (postType === "text") {
    moreDaysInput.removeAttribute("required");
    eventFields.forEach((field) => {
      field.removeAttribute("required");
    });

    textFields.forEach((field) => {
      field.setAttribute("required", true);
    });
  }
};

document.addEventListener("DOMContentLoaded", () => {
  if (window.location.pathname === "/") {
    initializePostTypeDisplay();
  }
  initializeEventListeners();
});

if (window.location.pathname === "/") {
  moreDaysCheckbox.addEventListener("click", () => {
    moreDaysLabel.classList.toggle("active");
    moreDaysInput.classList.toggle("active");
    if (moreDaysInput.classList.contains("active")) {
      moreDaysInput.setAttribute("required", true);
    } else {
      moreDaysInput.removeAttribute("required");
    }
  });
}
