var base_elemen;
(async () => {
	modul = await import('/static/js/content.js');
	content = new modul.Content_Handler();
	base_elemen = document.querySelector('#content')
	url = window.location
	console.log(url)
	if (url['pathname'] == "/"){
		const params = new URLSearchParams(url.search);
		if (params.get('page')){
			await content.Home(base_elemen, page=parseInt(params.get("page"), 10), current=parseInt(params.get("page"), 10), cari=params.get('s', ""));
		} else {
			await content.Home(base_elemen, page=1, current=1);
		}
		
	} else if (url['pathname'].split("/")[1] == 'player'){
		await content.Player(base_elemen, name=url['pathname'].split('/')[2]);
	}
	
	// async function GetDriver(){
		// const { Driver } = await import('/static/js/driver/HttpRequest/driver.js');
		// return Driver;
	// };
	
	
})();
