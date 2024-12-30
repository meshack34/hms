 function googleTranslateElementInit() {
    new google.translate.TranslateElement({
    pageLanguage: 'en',
    autoDisplay: 'true',
    layout: google.translate.TranslateElement.InlineLayout.HORIZONTAL
    }, 'google_translate_element');
    }
    function cancelTranslation() {
        var translate = google.translate.TranslateElement.getInstance();
        translate.restore();
    }
