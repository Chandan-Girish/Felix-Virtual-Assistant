$(document).ready(function () {
    
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        
        $(".felix-message li:first").text(message);
        $('.felix-message').textillate('start');
        
    }

    //Display or return to landing page
    eel.expose(ReturnLanding)
    function ReturnLanding() {

        $("#Landing").attr("hidden", false);
        $("#WaveEffect").attr("hidden", true);
    }

    //chat log 
    //Sender-Text (User query)
    eel.expose(senderText)
    function senderText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {

            chatBox.innerHTML  += `<div class = "row justify-content-end mb-4">
            <div class = "width-size">
            <div class = "sender_message">${message}</div>
            </div>`;

            // Scroll to the bottom of chat-box
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    }

    //Receiver-Text (Assistant Reply)
    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {

            chatBox.innerHTML  += `<div class = "row justify-content-start mb-4">
            <div class = "width-size">
            <div class = "receiver_message">${message}</div>
            </div>`;

            // Scroll to the bottom of chat-box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
});