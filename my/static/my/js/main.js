if (!window.WebSocket) alert("WebSocket not supported by this browser");


var communication = new Vue({
    el: '#Communion',
    data : {
        isCommunication : false,
        s : undefined,
        num_room : undefined,
        newmessage : undefined,
        oldmessage : undefined,
    },
    methods: {
        inRoom: function (message) {
            if(typeof(this.s) == 'object'){
                this.s.close();
            }
            this.num_room = message;


            var ws = new WebSocket('ws://' + window.location.host + '/chat-' + message +  '/');
            ws.onopen = function(){
                console.log("new connection - " + message);
            };
            ws.onmessage = function(e) {
                var username = document.getElementById('nameUser').innerHTML;
                var data = JSON.parse(e.data);
                
                if(data['preload']){
                    document.getElementById('messages').innerHTML = "";
                    var objects = JSON.parse(data['preload']);
                    for(var i = 0; i < objects.length; i++){
                        var isAuthor = null,
                            isYour = '';
                        if(username == objects[i].username){
                            isAuthor = "me"
                            isYour = '<i>you</i>'
                        }
                        else {
                            isAuthor = "they"
                        }
                        var div = '<div class="message">\
                                    <div class="' + isAuthor + ' style-mess">\
                                        <div class="username">'+isYour+'<span>' + objects[i].username + '</span></div>\
                                        <p>' + objects[i].message + '</p>\
                                    </div>\
                                    </div>';
                        document.getElementById('messages').innerHTML += div;
                        document.getElementById('messages').scrollTo(0, document.getElementById('messages').scrollHeight);
                    }
                };
                if(data['newmessage']){
                   var object = JSON.parse(data['newmessage']); 
                   if(object['isSend']){
                        var info = document.getElementById("info");
                        info.innerHTML = '';
                        var list = '',
                            n = 0;
                        var objectes = object['users'];
                        
                        for(var i = 0; i < objectes.length; i ++){
                            if(objectes[i].name != username){
                                list += objectes[i].name + ', ';
                                n += 1;
                            }
                        }
                        if(n > 0){
                            info.innerHTML = "Write now: " + list.substr(0, list.length - 2);
                            this.showInfo = true;
                        }
                        else {
                            this.showInfo = false;
                            info.innerHTML = '';
                        }
                   }
                   else {
                    var isAuthor = null,
                        isYour = '';
                        if(username == object.username){
                            isAuthor = "me"
                            isYour = "<i>you</i>"
                        }
                        else {
                            isAuthor = "they"
                        }
                        var div = '<div class="message">\
                                        <div class="' + isAuthor + ' style-mess">\
                                            <div class="username">'+isYour+'<span>' + object.username + '</span></div>\
                                            <p>' + object.message + '</p>\
                                        </div>\
                                        </div>';
                        document.getElementById('messages').innerHTML += div;
                        document.getElementById('messages').scrollTo(0, document.getElementById('messages').scrollHeight);
                    }
               };
               if(data['nomessage']){
                    document.getElementById('messages').innerHTML = '';
                    var div = document.createElement('div');
                    div.innerHTML = '<h1>No messages</h1>';
                    div.id = 'noMessage';
                    document.getElementById('messages').appendChild(div);    
               }
            }
            
            ws.onclose = function(e){
                console.log('close connection - ' + message);
            }
            ws.onerror = function(error) {
                alert(error.message);
            }
            this.isCommunication = true;
            this.s = ws;
        },
        toSend: function(id){
            var value = document.getElementById(id).value;
            if(value.length > 0){
                var username = document.getElementById('nameUser').innerHTML;
                var object = {
                    'message' : value,
                    'username' : username,
                    'room' : this.num_room,
                    'isSend' : false
                }
                this.s.send( JSON.stringify( { 'newmessage': object } ) );
            }
            document.getElementById(id).value = '';

        },
        inputText: function(){
            var value = document.getElementById('m_send').value;
            var username = document.getElementById('nameUser').innerHTML;
            if (value.length > 0){
                this.newmessage = value;
                var object = {
                    'username' : username,
                    'isSend' : true,
                    'room' : this.num_room
                }
                this.s.send( JSON.stringify( { 'writing' : object } ) );
            }
            else {
                var object = {
                    'username' : username,
                    'isSend' : false,
                    'room' : this.num_room
                }
                this.s.send( JSON.stringify( { 'writing' : object } ) );
            }
        },
        checkInput: function(){
            try { 
                var value = document.getElementById('m_send').value;
                if (value.length > 0){
                    this.newmessage = value;
                    if(this.newmessage == this.oldmessage){
                        var username = document.getElementById('nameUser').innerHTML;
                        var object = {
                            'username' : username,
                            'isSend' : false,
                            'room' : this.num_room
                        }
                        this.s.send( JSON.stringify( { 'writing' : object } ) );                        
                    }
                    else {
                        this.oldmessage = this.newmessage;
                    }
                } 
            }
            catch ( TypeError ){ }
        }
        
    },
    mounted: function(){
    }
});

var timerId = setInterval(function() {
    communication.checkInput()
  }, 2000);

