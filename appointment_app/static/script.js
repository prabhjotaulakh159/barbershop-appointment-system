window.onload = function() {
    setTimeout(function() {
        const element = document.getElementById('flashes');
        console.log(element);
        if (element) {
            element.parentNode.removeChild(element);
        }
    }, 3000); 
};