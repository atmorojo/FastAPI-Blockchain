if (localStorage.authToken == undefined) {
	let authToken = null;
} else {
	authToken = localStorage.authToken
}

// gate htmx requests on the auth token
htmx.on("htmx:confirm", (e)=> {
	console.log("coba")
	// if there is no auth token
	if(authToken == null) {
		// stop the regular request from being issued
		e.preventDefault() 
		// only issue it once the auth promise has resolved
		auth.then(() => e.detail.issueRequest()) 
	}
})

// add the auth token to the request as a header
htmx.on("htmx:configRequest", (e)=> {
	e.detail.headers["AUTH"] = authToken
})

function auth() {
}
