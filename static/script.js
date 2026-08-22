function confirmDelete() {
    return confirm("Are you sure you want to delete this item?");
}

document.addEventListener('DOMContentLoaded', function() {

    // --- Hamburger Menu ---
    const hamburger = document.getElementById('hamburger-menu');
    const navLinks = document.getElementById('nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('open');
        });
    }

    // --- Faculty Dropdown ---
    const facultySelect = document.getElementById('faculty_id');
    const deptSelect = document.getElementById('department_id');

    if (facultySelect && deptSelect) {
        facultySelect.addEventListener('change', function() {
            const facultyId = this.value;

            deptSelect.innerHTML = '<option value="">Select Department</option>';

            if (!facultyId) {
                return;
            }

            fetch(`/get_departments?faculty_id=${facultyId}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(dept => {
                        const option = document.createElement('option');
                        option.value = dept.id;
                        option.textContent = dept.name;
                        deptSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching departments:', error);
                    deptSelect.innerHTML = '<option value="">Error loading departments</option>';
                });
        });
    }

    // --- Auto-dismiss flash messages ---
    const flashMessages = document.querySelectorAll('.flash');

    flashMessages.forEach(function(flash) {
        try {
            setTimeout(function() {
                flash.classList.add('flash-removing');
                setTimeout(function() {
                    flash.remove();
                }, 300);
            }, 3000);
        } catch (e) {
            console.log("Flash removal handled gracefully.");
        }
    });

    // --- Password Visibility ---
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const eyeOpen = this.querySelector('.eye-open');
            const eyeOff = this.querySelector('.eye-off');

            if (input.type === 'password') {
                input.type = 'text';
                eyeOpen.style.display = 'none';
                eyeOff.style.display = 'block';
            } else {
                input.type = 'password';
                eyeOpen.style.display = 'block';
                eyeOff.style.display = 'none';
            }
        });
    });

});
