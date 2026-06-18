(function () {
  const grid = document.getElementById('grid');
  const searchInput = document.getElementById('search');
  const searchCount = document.getElementById('search-count');
  const empty = document.getElementById('empty');
  const emptyQuery = document.getElementById('empty-query');

  const modal = document.getElementById('modal');
  const modalImg = document.getElementById('modal-img');
  const modalTitle = document.getElementById('modal-title');
  const modalDesc = document.getElementById('modal-desc');
  const modalDims = document.getElementById('modal-dims');
  const modalWeight = document.getElementById('modal-weight');
  const modalStatus = document.getElementById('modal-status');
  const modalCta = document.getElementById('modal-cta');

  let works = [];

  function renderGrid() {
    grid.innerHTML = '';
    works.forEach((work, i) => {
      const tile = document.createElement('button');
      tile.className = 'tile';
      tile.dataset.index = i;
      tile.dataset.title = work.title.toLowerCase();
      tile.setAttribute('aria-label', work.title);

      const img = document.createElement('img');
      img.src = work.image;
      img.alt = work.title;
      img.loading = 'lazy';
      tile.appendChild(img);

      tile.addEventListener('click', () => openModal(work));
      grid.appendChild(tile);
    });
  }

  function applySearch() {
    const q = searchInput.value.trim().toLowerCase();
    const tiles = Array.from(grid.children);
    let visible = 0;

    tiles.forEach(tile => {
      const match = !q || tile.dataset.title.includes(q);
      tile.classList.toggle('is-hidden', !match);
      if (match) visible++;
    });

    searchCount.textContent = q ? `${visible}/${works.length}` : '';
    empty.classList.toggle('hidden', !(q && visible === 0));
    emptyQuery.textContent = searchInput.value.trim();
  }

  function openModal(work) {
    modalImg.src = work.image;
    modalImg.alt = work.title;
    modalTitle.textContent = work.title;
    modalDesc.textContent = work.description || '';
    modalDims.textContent = work.dimensions ? `Dimensions: ${work.dimensions}` : '';
    modalWeight.textContent = work.weight ? `Weight: ${work.weight}` : '';

    const status = work.status || 'Available';
    modalStatus.textContent = status;
    modalStatus.className = 'badge' + (/sold/i.test(status) ? ' sold' : /not available/i.test(status) ? ' unavailable' : '');

    const subject = encodeURIComponent(`Inquiry: ${work.title}`);
    modalCta.href = `mailto:info@cheglakovart.com?subject=${subject}`;
    modalCta.style.display = /sold/i.test(status) ? 'none' : 'block';

    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
  }

  function closeModal() {
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
  }

  modal.addEventListener('click', (e) => {
    if (e.target.dataset.close !== undefined) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });

  searchInput.addEventListener('input', applySearch);

  fetch('data.json')
    .then(res => res.json())
    .then(data => {
      works = data;
      renderGrid();
      applySearch();
    })
    .catch(err => {
      grid.innerHTML = `<p style="color:#A8967E">Failed to load works: ${err.message}</p>`;
    });
})();
