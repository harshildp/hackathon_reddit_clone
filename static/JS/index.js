<<<<<<< HEAD
$(document).ready(function(){
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
    var bgImageArray = ["lonely.jpg", "uluwatu.jpg", "carezza-lake.jpg", "batu-bolong-temple.jpg"],
    base = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/4273/full-",
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
=======
$(document).ready(function(){
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
    var bgImageArray = ["lonely.jpg", "uluwatu.jpg", "carezza-lake.jpg", "batu-bolong-temple.jpg"],
    base = "https://s3-us-west-2.amazonaws.com/s.cdpn.io/4273/full-",
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
>>>>>>> 506499f6d8dc47805164ed9b9e46c7f00a8bcd5e
});