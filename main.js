function initialize(){
    fetch('/getLocation').then((res) => {
        return res.json()
    }).then(processData);
}

function processData(data){
    const geocoder = new google.maps.Geocoder();
    const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 24.1223416, lng: 120.6742643},
        zoom: 8
    });

    let timer = 0
    data.forEach((e) => {
        setTimeout(()=>{
            codeAddress(e);
        }, timer);
        timer += 100;
    });

    function codeAddress(data) {
            geocoder.geocode({ 'address': data.address }, (res, status) => {
                if (status == google.maps.GeocoderStatus.OK) {
                    map.setCenter(res[0].geometry.location);
                    const infowindow = new google.maps.InfoWindow({
                        content: `${data.address}`
                    })
                    let marker = new google.maps.Marker({
                        map: map,
                        position: res[0].geometry.location,
                        title: `address:${data.address}\nname:${data.name}`,
                        animation: google.maps.Animation.DROP
                    });
                    marker.addListener('click', () => {
                        window.open(`highchart.html?add=${data.address}`, data.address, config='height=400, width=600');
                        // infowindow.open(map, marker);
                    });
                } else if (status == google.maps.GeocoderStatus.OVER_QUERY_LIMIT) {
                    setTimeout(() => {
                        codeAddress(data);
                    }, 500);
                } else {
                    console.log('geocoder error()',data, res, status);
                }
            });
    }
}

window.onload = ()=>{
    initialize();
}