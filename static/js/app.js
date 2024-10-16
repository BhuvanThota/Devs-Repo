let alertWrappers = document.querySelectorAll('.alert');

for (const alertWrapper of alertWrappers) {
  let alertClose = alertWrapper.querySelector('.alert__close');

  if (alertClose) {
    alertClose.addEventListener('click', () => {
      alertWrapper.style.display = 'none';
    });
  }
}
