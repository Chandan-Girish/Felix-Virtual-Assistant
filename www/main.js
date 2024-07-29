$(document).ready(function () {
    
    $('.anitext').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        }
    });

    /* Wave Effect Start */
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart : true,
      });

    /* Wave Effect End */

    /* Nova message animation */
    $('.felix-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true
        }
    });

    /*End Message*/

    //Mic button functionality
    $('#MicBtn').click(function () { 
        eel.playAssistantSound()
        $('#Landing').attr("hidden", true);
        $('#WaveEffect').attr("hidden", false);
        eel.allCommands()()
    });

    // Shortcut key function to activate the assistant
    function doc_keyUp(e) {

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $('#Landing').attr("hidden", true);
            $('#WaveEffect').attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    /* Test box functionality start */
    function PlayAssistant(message) {

        if (message != "") {

            $("#Landing").attr("hidden", true);
            $("#WaveEffect").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("");
            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);

        }
        
    }

    function ShowHideButton(message) {

        if (message.length == 0) {

            $("#MicBtn").attr("hidden", false);
            $("#SendBtn").attr("hidden", true);

        }
        else {

            $("#MicBtn").attr("hidden", true);
            $("#SendBtn").attr("hidden", false);

        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)

    });

    $("#SendBtn").click(function () {

        let message = $("#chatbox").val();
        PlayAssistant(message)
        
    });

    $("#chatbox").keypress(function (e) {

        key = e.which;
        if (key == 13) {
            
            let message = $("#chatbox").val()
            PlayAssistant(message)

        }
    });
    /* Text box functionality end*/

});