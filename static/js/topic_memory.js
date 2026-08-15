/**
 * LearningHub — Topic Detail, Personal Learning Memory & Progress AJAX Script
 */

document.addEventListener('DOMContentLoaded', () => {
  initMemoryAutoSave();
  initUnderstandingSelector();
  initCompletionToggle();
  initBookmarkButtons();
});

// 1. Personal Learning Memory Save
function initMemoryAutoSave() {
  const memoryForm = document.getElementById('personal-memory-form');
  const saveBtn = document.getElementById('save-memory-btn');
  const statusTag = document.getElementById('memory-status-indicator');

  if (!memoryForm || !saveBtn) return;

  saveBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const topicId = memoryForm.getAttribute('data-topic-id');
    const url = `/memory/save/${topicId}/`;
    const formData = new FormData(memoryForm);

    if (statusTag) statusTag.innerText = 'Saving...';
    saveBtn.disabled = true;

    fetch(url, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(res => res.json())
    .then(data => {
      saveBtn.disabled = false;
      if (data.status === 'ok') {
        if (statusTag) {
          statusTag.innerText = `Saved (${data.updated_at})`;
          statusTag.style.color = 'var(--accent-emerald)';
        }
      }
    })
    .catch(err => {
      saveBtn.disabled = false;
      if (statusTag) {
        statusTag.innerText = 'Save error. Retry.';
        statusTag.style.color = 'var(--accent-rose)';
      }
    });
  });
}

// 2. Understanding Level Selector
function initUnderstandingSelector() {
  const selectorGroup = document.querySelector('.understanding-selector');
  if (!selectorGroup) return;

  const topicId = selectorGroup.getAttribute('data-topic-id');
  const buttons = selectorGroup.querySelectorAll('.level-btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const levelVal = btn.getAttribute('data-level');
      
      const formData = new FormData();
      formData.append('understanding_level', levelVal);

      fetch(`/progress/update/${topicId}/`, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          buttons.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }
      });
    });
  });
}

// 3. Mark Topic Completed Toggle
function initCompletionToggle() {
  const toggleBtn = document.getElementById('toggle-completion-btn');
  if (!toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    const topicId = toggleBtn.getAttribute('data-topic-id');
    const isCompleted = toggleBtn.getAttribute('data-completed') === 'true';
    const newStatus = !isCompleted;

    const formData = new FormData();
    formData.append('is_completed', newStatus ? 'true' : 'false');

    fetch(`/progress/update/${topicId}/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === 'ok') {
        toggleBtn.setAttribute('data-completed', data.is_completed ? 'true' : 'false');
        if (data.is_completed) {
          toggleBtn.classList.remove('btn-outline');
          toggleBtn.classList.add('btn-success');
          toggleBtn.innerHTML = '✓ Completed';
        } else {
          toggleBtn.classList.remove('btn-success');
          toggleBtn.classList.add('btn-outline');
          toggleBtn.innerHTML = 'Mark as Completed';
        }
      }
    });
  });
}

// 4. Bookmark Toggle on Resources
function initBookmarkButtons() {
  document.querySelectorAll('.bookmark-toggle-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const resId = btn.getAttribute('data-resource-id');
      const url = `/learning/resources/${resId}/bookmark/?format=json`;

      fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          if (data.is_bookmarked) {
            btn.classList.add('active');
            btn.innerHTML = '★ Saved';
          } else {
            btn.classList.remove('active');
            btn.innerHTML = '☆ Bookmark';
          }
        }
      });
    });
  });
}
