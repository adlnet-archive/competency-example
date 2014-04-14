(function(ADL){
    
    var debug = true;
    var log = function(message)
    {
        if (!debug) return false;
        try
        {
            console.log(message);
            return true;
        }
        catch(e){return false;}
    }

    function getcomps(comp) {
        if (comp) {
            if (comp instanceof Array){
                var ret = [];
                for(var i = 0; i < comp.length; i++){
                    ret.push({"id": comp[i]})
                }
                return ret;
            }
            return [{"id": comp}];
        }
        return [];
    } 

    function PopcornVideo(player, comp) {
        var myplayer = player;
        var playerID = player.media.id;
        var firstQuartileHit = false;
        var halfwayHit = false;
        var thirdQuartileHit = false;
	var ended = false;
        var isTracking = true;
        var comparray = getcomps(comp);
        var hascompetency = comp;

        // Youtube videos don't have children
        var objectURI = player.media.children[0].src ? player.media.children[0].src : player.media.src;
        var videoActivity = {"id":objectURI};
        
        // Edit the actor inside of the wrapper or just include it here
        var getactor = function() {
            return ADL.XAPIWrapper.lrs.actor ? ADL.XAPIWrapper.lrs.actor :
            {"account":{"name":"tester", "homePage":"uri:testaccount"}};
        };

        // Play event
        myplayer.on("play", function(){
            var currentTime = myplayer.currentTime()
            // This if is a youtube workaround - when replaying youtube vids the roundTime is the same as the duration
            if (currentTime == Math.round(myplayer.duration())){
                log('youtube video ' + playerID + ' launched weird')
                startstuff(true)
            }
            // Playing after pause
            else if (currentTime != 0){
                log('video ' + playerID + ' resumed')
                startstuff(false)
            }
            // Normal start when vid is launched
            else{
                log('video ' + playerID + ' launched')
		ended = false;
                startstuff(true)
            }
        });

        // Every second event
        myplayer.on("timeupdate", function(){
            var currentTime = myplayer.roundTime()
            // If stmt to catch specific times - the hits get reset to false when video ends
            if (!firstQuartileHit && currentTime == Math.round(myplayer.duration() * .25)){
                log('video ' + playerID + ' first point')
                firstQuartileHit = true
                middleStuff("firstquartile", currentTime)
            }
            else if (!halfwayHit && currentTime == Math.round(myplayer.duration() * .5)){
                log('video ' + playerID + ' half point')
                halfwayHit = true
                middleStuff("halfway", currentTime)
            }
            else if (!thirdQuartileHit && currentTime == Math.round(myplayer.duration() * .75)){
                log('video ' + playerID + ' third point')
                thirdQuartileHit = true
                middleStuff("thirdquartile", currentTime)
            }
        });

        // Pause event
        myplayer.on("pause", function(){
            var currentTime = myplayer.roundTime()
            // If stmt is a youtube workaround - youtube vids pause right before they end
            if (currentTime != Math.round(myplayer.duration())){
                log('video ' + playerID + ' paused')
                pauseStuff(currentTime)
            }
         });

        // Seeked event
        myplayer.on("seeked", function(){
            var currentTime = myplayer.roundTime()
            // If try to replay movie, instead of playing it fires seeked
            if (currentTime != 0){
                log('seeked ' + playerID + ' to ' + currentTime)
                seekStuff(currentTime)
            }
            // Youtube workaround - videos seek to 0 when replayed or launched
            else{
                log('seeked to 0s so really launched ' + playerID)
                startstuff(true)
                // Reset video quartile states
                firstQuartileHit = halfwayHit = thirdQuartileHit = false;
            }
        });

        // Ended event
        myplayer.on("ended", function(){
            log('video ' + playerID + ' ended')
            endStuff(myplayer.duration())
        });    

        function startstuff(launched){
            var stmt = {"actor":getactor(), "object": videoActivity}
            if (hascompetency){
                stmt["context"] = {"contextActivities":{"other" : comparray}}
            }

            if (launched){
                stmt["verb"] = ADL.verbs.launched
            }
            else{
                var resumeTime = "PT" + myplayer.roundTime() + "S";
                stmt["verb"] = ADL.verbs.resumed
                stmt["result"] = {"extensions":{"resultExt:resumed":resumeTime}}
            }
            report(stmt);
        }

        function middleStuff(quartile, benchTime) {
            var benchObj = {"id":objectURI + "#" + quartile};
            var bench = "PT" + benchTime + "S";
            var extKey = "resultExt:" + quartile
            var result = {"extensions":{}};
            

            var stmt = {"actor":getactor(),
                    "verb":ADL.verbs.progressed,
                    "object":benchObj,
                    "result":result}
            var context = {"contextActivities":{"parent":[{"id": objectURI}]}};
            
            if (hascompetency){
                context["contextActivities"]["other"] = comparray;
            }
            stmt["context"] = context
            result["extensions"][extKey] = bench
            report(stmt);
        }

        function pauseStuff(pauseTime){
            var paused = "PT" + pauseTime + "S";
            var stmt = {"actor":getactor(), 
                    "verb":ADL.verbs.suspended,
                    "object":videoActivity, 
                    "result":{"extensions":{"resultExt:paused":paused}}}

            if (hascompetency){
                stmt["context"] = {"contextActivities":{"other" : comparray}}
            }
            report(stmt);
        }

        function seekStuff(seekTime){
            var seeked = "PT" + seekTime + "S";
            var stmt = {"actor":getactor(), 
                    "verb":ADL.verbs.interacted,
                    "object":videoActivity, 
                    "result":{"extensions":{"resultExt:seeked": seeked}}}
            
            if (hascompetency){
                stmt["context"] = {"contextActivities":{"other" : comparray}}
            }             
            report(stmt);
        }

        function endStuff(endTime) {
 	    if (ended) return;
	    ended = true;
            var duration = "PT" + Math.round(endTime) + "S";
            var stmt = {"actor":getactor(), 
                    "verb":ADL.verbs.completed, 
                    "object":videoActivity, 
                    "result":{"duration":duration, "completion": true}}

            if (hascompetency){
                stmt["context"] = {"contextActivities":{"other" : comparray}};
                
                var stmtpassed = {"actor":getactor(), 
                    "verb":ADL.verbs.passed, 
                    "object":videoActivity, 
                    "result":{"duration":duration, "completion": true},
                    "context":{"contextActivities":{"other" : comparray}}}
                multireport([stmt, stmtpassed], function(r){console.log(r)});
            }
	    else {
               report(stmt);
	    }
            // Reset video quartile states
            firstQuartileHit = halfwayHit = thirdQuartileHit = false;
        }

	this.multireport = multireport;
	function multireport (stmt, callback) {
	   if (stmt) {
		for(var i = 0; i < stmt.length; i++)                
			stmt[i]['timestamp'] = (new Date()).toISOString();
                if (isTracking) {
                    ADL.XAPIWrapper.sendStatements(stmt, callback);
                }
                else {
                    log("would send this statement if 'isTracking' was true.");
                    log(stmt);
                }
            }	
	}

        this.report = report;
        function report (stmt) {
            if (stmt) {
                stmt['timestamp'] = (new Date()).toISOString();
                if (isTracking) {
                    ADL.XAPIWrapper.sendStatement(stmt, function(){});
                }
                else {
                    log("would send this statement if 'isTracking' was true.");
                    log(stmt);
                }
            }
        }
    };

    // -- -- //
    var XAPIVideo = function() {
        this._videos = {};
    };

    XAPIVideo.prototype.addVideo = function(player, comp) {
        try{
            var playerID = player.media.id
            var v = new PopcornVideo(player, comp)
        }
        catch(e){
            throw "Cannot add video: " + e.message;
        }        
        this._videos[playerID] = v;
        return true;
    };

    XAPIVideo.prototype.getVideo = function(id) {
        try {
            return this._videos[id]
        }
        catch (e) {
            return {};
        }
    };

    XAPIVideo.prototype.getVideos = function() {
        var v = []
        for (var k in this._videos) {
            v.push(k);
        }
        return v;
    };

    ADL.XAPIVideo = new XAPIVideo();

}(window.ADL = window.ADL || {}));
