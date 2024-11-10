document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.option');

    options.forEach(option => {
      const headerInput = option.querySelector('.header-input');
      const subOption = option.querySelector('.sub-option');
      const caretUp = option.querySelector('#caret-up');
      const caretDown = option.querySelector('#caret-down');

      const toggleSubOption = () => {
        if (headerInput.checked) {
          subOption.style.display = 'block';
          caretUp.style.display = 'inline-block';
          caretDown.style.display = 'none';
        } else {
          subOption.style.display = 'none';
          caretUp.style.display = 'none';
          caretDown.style.display = 'inline-block';
        }
      };

      toggleSubOption();

      headerInput.addEventListener('change', () => {
        options.forEach(otherOption => {
            if (otherOption !== option) {
                const otherHeaderInput = otherOption.querySelector('.header-input');
                otherHeaderInput.checked = false;
                otherOption.querySelector('.sub-option').style.display = 'none';
                otherOption.querySelector('#caret-up').style.display = 'none';
                otherOption.querySelector('#caret-down').style.display = 'inline-block';
            }
            });

            toggleSubOption();
        });


    });
});

