// Flash for 5 seconds and then go away
window.onload = function() {
    setTimeout(function() {
        const element = document.getElementById('flashes');
        if (element) {
            element.parentNode.removeChild(element);
        }
    }, 5000); 
};