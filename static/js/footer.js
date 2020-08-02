
$(function(){
    function footBackgroundColorChange(){
        let footcolorDict = {
            'index':'rgb(235,205,174)',
            'list':'rgb(97,100,101)',
            'read':'rgb(217,95,92)',
            'link':'rgb(43,28,21)',
            'create':'rgb(97,100,101)',
            'user':'rgb(70,100,69)',
            'update':'rgb(97,100,101)',
            'notice':'rgb(66,113,67)',
        };
        let headcolorDict = {
            'index':'rgba(235,205,174,.1)',
            'list':'rgba(97,100,101,.1)',
            'read':'rgba(217,95,92,.1)',
            'link':'rgba(43,28,21,.1)',
            'create':'rgba(97,100,101,.1)',
            'user':'rgba(70,100,69,.1)',
            'update':'rgba(97,100,101,.1)',
            'notice':'rgba(66,113,67,.1)',
        };
        let backgroundImg = {
            'index':'ToxicValley.png',
            'list':'SavageDivide.png',
            'read':'CranberryBog.png',
            'link':'AshHeap.png',
            'create':'SavageDivide.png',
            'user':'TheMire.png',
            'update':'SavageDivide.png',
            'notice':'TheForest.png',
        };
        let CurrentURL = window.location.href;
        str1 = CurrentURL.split('/');
        let obody = $('body');
        if (str1[3] === 'index' || str1[3] === ''){
            obody.css('overflow','hidden');
        }
        if(str1[3] != ''){
            obody.css('background',"url('../../static/imgs/"+backgroundImg[str1[3]]+"') no-repeat center");
            // $('footer').css('cssText','background:'+footcolorDict[str1[3]]+'!important;');
        }else{
            obody.css('background',"url('../../static/imgs/"+backgroundImg["index"]+"') no-repeat center");
        }
        $('footer').css('cssText','background:'+'none!important');
        obody.css('backgroundSize','cover');
        obody.css('height','100vh');
        $('.navbar').css('cssText','background:'+headcolorDict[str1[3]]+'!important;');
    }
    footBackgroundColorChange();
    $(window).resize(footBackgroundColorChange);
})
