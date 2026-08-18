document.addEventListener('DOMContentLoaded', () => {
  const startTime = document.querySelector('[data-start-time]');
  const duration = document.querySelector('[data-duration]');
  const estimate = document.getElementById('cost-estimate');
  const detail = document.getElementById('cost-detail');
  const naira = new Intl.NumberFormat('en-NG');

  function updateDurations() {
    if (!startTime || !duration) return;
    const hour = Number(startTime.value.split(':')[0]);
    const current = Number(duration.value) || 1;
    const maximum = 18 - hour;
    duration.innerHTML = '';
    for (let hours = 1; hours <= maximum; hours++) {
      const option = new Option(`${hours} hour${hours > 1 ? 's' : ''}`, hours, false, hours === Math.min(current, maximum));
      duration.add(option);
    }
    updateCost();
  }
  function updateCost() {
    if (!duration || !estimate) return;
    const hours = Number(duration.value) || 1;
    estimate.textContent = `₦${naira.format(hours * 10000)}`;
    detail.textContent = `${hours} hour${hours > 1 ? 's' : ''} × ₦10,000`;
  }
  startTime?.addEventListener('change', updateDurations);
  duration?.addEventListener('change', updateCost);
  updateCost();
  document.querySelector('.modal-close')?.addEventListener('click', () => document.querySelector('.modal-backdrop').remove());
});
