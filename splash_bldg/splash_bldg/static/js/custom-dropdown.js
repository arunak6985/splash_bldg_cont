// Custom Dropdown Component
function initCustomDropdowns() {
    $('select.custom-select').each(function() {
        if (!$(this).next().hasClass('custom-dropdown')) {
            var selected = $(this).find('option:selected');
            var placeholder = $(this).data('placeholder') || 'Select option';
            var displayText = selected.length ? selected.text() : placeholder;
            
            $(this).after('<div class="custom-dropdown"><span class="current">' + displayText + '</span><div class="dropdown-list"><div class="search-box"><input type="text" class="search-input" placeholder="Search..."></div><ul></ul></div></div>');
            
            var dropdown = $(this).next();
            var options = $(this).find('option');
            
            options.each(function() {
                if ($(this).val()) {
                    dropdown.find('ul').append('<li class="option" data-value="' + $(this).val() + '">' + $(this).text() + '</li>');
                }
            });
        }
    });
}

// Dropdown events
$(document).on('click', '.custom-dropdown', function(e) {
    if ($(e.target).hasClass('search-input')) return;
    $('.custom-dropdown').not($(this)).removeClass('open');
    $(this).toggleClass('open');
    if ($(this).hasClass('open')) {
        $(this).find('.search-input').val('').focus();
        $(this).find('.option').show();
    }
});

$(document).on('click', '.custom-dropdown .option', function() {
    var value = $(this).data('value');
    var text = $(this).text();
    $(this).closest('.custom-dropdown').find('.current').text(text);
    $(this).closest('.custom-dropdown').prev('select').val(value).trigger('change');
    $(this).closest('.custom-dropdown').removeClass('open');
});

$(document).on('input', '.custom-dropdown .search-input', function() {
    var searchTerm = $(this).val().toLowerCase();
    $(this).closest('.dropdown-list').find('.option').each(function() {
        $(this).toggle($(this).text().toLowerCase().includes(searchTerm));
    });
});

$(document).on('click', function(e) {
    if (!$(e.target).closest('.custom-dropdown').length) {
        $('.custom-dropdown').removeClass('open');
    }
});

// Initialize on document ready
$(document).ready(function() {
    initCustomDropdowns();
});