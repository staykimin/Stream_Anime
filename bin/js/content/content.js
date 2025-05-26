let intervalId, driver;

export class Content_Handler{
	constructor(delay, data){
		this.delay = delay;
	}
	
	async GetDriver(){
		const { Driver } = await import('../driver/HttpRequest/driver.js');
		return Driver
	}
	Delay(ms){
		return new Promise(resolve => setTimeout(resolve, ms));
	}
	
	async GetDevice(){
		driver = await this.GetDriver()
		let respon = new driver(
			"/api/v1/device", "post", {'Accept': 'application/json', 'Content-Type': 'application/json'}, {"id_user":id_user, 'mode':'get'}
		);
		let data = await respon.Execute();
		if (data['status'] && data['data']['status']){
			// console.log(data['data']['data'])
			await this.GenerateTabel(data['data']['data'])
		}
	}
	
	async GenerateQR(){
		let respon = new driver(
			'/api/v1/device', 'post', {'Accept': 'application/json', 'Content-Type': 'application/json'}, {"id_user":id_user, 'mode':'qr', 'nomor':document.querySelector("#nomor").value}
		);
		let data = await respon.Execute();
		if (data['status'] && data['data']['status']){
			console.log(data['data']['data'][0]['qr'])
		}
		// var inputString = $('#nomor').val();
		// $('#qrcode').empty(); // Hapus QR code sebelumnya
		// if (inputString) {
			// $('#qrcode').qrcode({
				// text: `${inputString}${document.querySelector('#nama').value}`,
				// width: 250, // Lebar QR Code
				// height: 250 // Tinggi QR Code
			// });
		// }
			
			// }
		// });
		// });
	}
	// async GenQR(driver){
		// let respon = new driver()
	// }
	async AddDevice(){
		document.querySelector('#connectBtn').addEventListener('click', async () => {
			driver = await this.GetDriver();
			let respon = new driver(
				"/api/v1/device", "post", {'Accept': 'application/json', 'Content-Type': 'application/json'}, {'nomor':document.querySelector('#nomor').value, "nama":document.querySelector('#nama').value, 'mode':'add', 'id_user':id_user}
			);
			let data = await respon.Execute();
			console.log(data)
			if (data['status'] && data['data']['status']){
				document.querySelector("#nomor").disabled = true;
				setInterval(this.GenerateQR, 5000);
				// alert('Data Berhasil Ditambahkan')
				// window.location.href = '/'
			} else {
				alert(data['data']['data']['error'])
			}
		});
		// await this.GenerateQR()
	}
	
	async Hapus(id){
		driver = await this.GetDriver()
		let respon = new driver(
			"/api/v1/device", "post", {'Accept': 'application/json', 'Content-Type': 'application/json'}, {'id_device':id, "id_user":id_user, 'mode':'delete'}
		);
		let data = await respon.Execute();
		if (data['status'] && data['data']['status']){
			window.location.href = '/'
		} else {
			alert(data['data']['data']['error'])
		}
	}
	
	async GenerateTabel(data){
		let tmp =``
		data['result'].forEach((item, index) => {
			tmp += `
				<tr>
				<td>${item['id']}</td>
				<td>${item['nomor']}</td>
				<td>${item['nama'] !== null && item['nama'].length > 0 ? item['nama'] : "No Name"}</td>
				<td>${item['error'] !== null ? item['error'] : "No Error"}</td>
				<td>${item['created_at']}</td>
				<td>
					<button class='btn btn-warning'>
						<i class="nav-icon fas fa-edit"></i>
					</button>
					<button class='btn btn-info'>
						<i class="nav-icon">
							<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16">
								<path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
								<path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
							</svg>
						</i>
					</button>
					<button id='delete-${item['id']}' class="btn btn-danger">
						<i class="nav-icon fas fa-trash"></i>
					</button>
				</td>
		  </tr>
			`
		})
		
		let tambah = document.getElementById("tambah");
		if (tambah){
			if (tambah.getAttribute('data-type') == 'device'){
				tambah.addEventListener('click', () => {
					window.location.href = '/add-device'
				})
			}
		}
		document.getElementById("data-tabel").getElementsByTagName('tbody')[0].innerHTML = tmp;
		data['result'].forEach((item) => {
			document.getElementById(`delete-${item['id']}`).addEventListener('click', () => this.Hapus(item['id']));
		});
	}
	
}