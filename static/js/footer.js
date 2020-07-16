
$(function(){
    function footBackgroundColorChange(){
        let footcolorDict = {
            'index':'rgb(235,205,174)',
            'list':'rgb(97,100,101)',
            'read':'rgb(217,95,92)',
            'link':'rgb(70,100,69)',
            'create':'rgb(97,100,101)',
            'user':'rgb(70,100,69)',
            'update':'rgb(97,100,101)',
            'notice':'rgb(70,100,69)',
        };
        let headcolorDict = {
            'index':'rgba(235,205,174,.1)',
            'list':'rgba(97,100,101,.1)',
            'read':'rgba(217,95,92,.1)',
            'link':'rgba(70,100,69,.1)',
            'create':'rgba(97,100,101,.1)',
            'user':'rgba(70,100,69,.1)',
            'update':'rgba(97,100,101,.1)',
            'notice':'rgba(70,100,69,.1)',
        };
        let backgroundImg = {
            'index':'ToxicValley.png',
            'list':'SavageDivide.png',
            'read':'CranberryBog.png',
            'link':'TheMire.png',
            'create':'SavageDivide.png',
            'user':'TheMire.png',
            'update':'SavageDivide.png',
            'notice':'TheMire.png',
        };
        let CurrentURL = window.location.href;
        str1 = CurrentURL.split('/');
        let obody = $('body');
        if(str1[3] != ''){
            obody.css('background',"url('../../static/imgs/"+backgroundImg[str1[3]]+"') no-repeat center");
            $('footer').css('cssText','background:'+footcolorDict[str1[3]]+'!important;');        
        }else{
            
            obody.css('background',"url('../../static/imgs/"+backgroundImg["index"]+"') no-repeat center");
            $('footer').css('cssText','background:'+footcolorDict['index']+'!important;');
        }
        obody.css('backgroundSize','cover');
        obody.css('height','100vh');
        $('.navbar').css('cssText','background:'+headcolorDict[str1[3]]+'!important;');
    }
    footBackgroundColorChange();
    $(window).resize(footBackgroundColorChange);
})
