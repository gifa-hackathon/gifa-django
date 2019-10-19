// Static Datatable
const data = 
[
        {
            "first_name": "Cecep",
            "last_name": "Adi",
            "phone": "082213541291",
            "age": 32,
            "blood_type": "B",
            "gender": "M",
            "disability_status": "-",
            "occupation": "farmer"

        },
        {
            "first_name": "Roby",
            "last_name": "Fauzi",
            "phone": "082213541291",
            "age": 19,
            "blood_type": "B",
            "gender": "M",
            "disability_status": "-",
            "occupation": "student"
        },
        {
            "first_name": "Irsyad",
            "last_name": "Kharisma",
            "phone": "082213541334",
            "age": 32,
            "blood_type": "B",
            "gender": "M",
            "disability_status": "-",
            "occupation": "youtuber"
        },
        {

            "first_name": "Agung",
            "last_name": "Pratikno",
            "phone": "082213541288",
            "age": 22,
            "blood_type": "B",
            "gender": "M",
            "disability_status": "-",
            "occupation": ""
        },
        {

            "first_name": "Panji",
            "last_name": "Kharisma",
            "phone": "082213541555",
            "age": 27,
            "blood_type": "B",
            "gender": "M",
            "disability_status": "-",
            "occupation": "PNS"
        },
        {

            "first_name": "Bimo",
            "last_name": "Pratikno",
            "phone": "082213541288",
            "age": 37,
            "blood_type": "B",
            "gender": "M",
            "disability_status": "-",
            "occupation": "-"
        },
        {

            "first_name": "Faizal",
            "last_name": "Pratikno",
            "phone": "082213541288",
            "age": 20,
            "blood_type": "AB",
            "gender": "M",
            "disability_status": "-",
            "occupation": "student"
        },
        {

            "first_name": "Hendra",
            "last_name": "Yahya",
            "phone": "082213541329",
            "age": 17,
            "blood_type": "A",
            "gender": "M",
            "disability_status": "-",
            "occupation": "student"
        },
 ]

// Jquery Listener
$(document).ready(function () {
	// Initiate the data table
    $('#disaster_table').DataTable({
    	responsive: true,
    	select: true,
    	data: data,
    	dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf'
        ],
    	/*
	        ajax: {
	  	      url: 'http://localhost:8000/api/entry/?format=json',
	        },
    	*/
    	columns	: [
    		{data: "first_name"},
    		{data: "last_name"},
    		{data: "phone"},
    		{data: "age"},
    		{data: "blood_type"},
    		{data: "gender"},
    		{data: "disability_status"},
    		{data: "occupation"}
    	]
    });
});



