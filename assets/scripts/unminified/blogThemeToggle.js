$('#dark-toggle').on('click', () => {
    if ($('#dark-toggle').prop('checked')) {
        $('#light-theme-link').removeAttr('disabled');
        $('#dark-theme-link').attr('disabled', 'disabled');
    } else {
        $('#light-theme-link').attr('disabled', 'disabled');
        $('#dark-theme-link').removeAttr('disabled');
    }
})