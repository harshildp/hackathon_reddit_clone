$(document).ready(function(){
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
    var bgImageArray = ["Space1.jpg", "Space2.jpg", "Space3.jpg", "Space4.jpg", "Space5.jpg"],
    base = "static/CycleImages/",
    secs = 4;
    bgImageArray.forEach(function(img){
        new Image().src = base + img;
        // caches images, avoiding white flash between background replacements
    });

    function backgroundSequence() {
        window.clearTimeout();
        var k = 0;
        for (i = 0; i < bgImageArray.length; i++) {
            setTimeout(function(){
                document.documentElement.style.background = "url(" + base + bgImageArray[k] + ") no-repeat center center fixed";
                document.documentElement.style.backgroundSize ="cover";
                document.documentElement.style.transition= '3s';
            if ((k + 1) === bgImageArray.length) { setTimeout(function() { backgroundSequence() }, (secs * 1000))} else { k++; }
            }, (secs * 1000) * i)
        }
    }
    backgroundSequence();
});
