document.getElementById("file").addEventListener("change",(e)=>{
		let size = e.target.files[0].size;
		document.getElementById("size").value=parseInt((size/1024)/1024);
		document.getElementById("type").value=e.target.files[0].type
})
