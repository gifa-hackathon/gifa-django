// Static Datatable
const data = 
[
        {
            "householder_name": "Cecep",
            "clothing": 12,
            "blankets": 1,
            "sleeping_mats": 1,
            "bathing_soap": 3,
            "sanitary": "-",
            "diapers": "-",
            "cooking_pot": 1,
            "plate": 1,
            "spoon": 3,
            "water": "10 lt",
            "food": "rice 10 kg"
        },
        {
            "householder_name": "Agus",
            "clothing": 12,
            "blankets": 3,
            "sleeping_mats": "-",
            "bathing_soap": 5,
            "sanitary": "-",
            "diapers": "-",
            "cooking_pot": 1,
            "plate": 2,
            "spoon": 3,
            "water": "20 lt",
            "food": "rice 5 kg"
        }
 ]

 // Initiate the data table
$(document).ready(function () {
    $('#humanitarian_aid').DataTable({
    	data: data,
    	/*
	        ajax: {
	  	      url: 'http://localhost:8000/api/entry/?format=json',
	        },
    	*/
    	columns	: [
    		{data: "householder_name"},
            {data: "clothing"},
            {data: "blankets"},
            {data: "sleeping_mats"},
            {data: "bathing_soap"},
            {data: "sanitary"},
            {data: "diapers"},
            {data: "cooking_pot"},
            {data: "plate"},
            {data: "spoon"},
            {data: "water"},
            {data: "food"}
    	]
    });
});

