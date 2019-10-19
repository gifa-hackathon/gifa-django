// Static Datatable
const data = 
[
        {
            "householder_name": "Cecep",
            "clothing": "082213541291",
            "blankets": 32,
            "sleeping_mats": "B",
            "bathing_soap": "M",
            "sanitary": "-",
            "diapers": "farmer",
            "cooking_pot": "farmer",
            "plate": "farmer",
            "spoon": "farmer",
            "water": "farmer",
            "food": "farmer"
        },
        {
            "householder_name": "Cecep",
            "clothing": "082213541291",
            "blankets": 32,
            "sleeping_mats": "B",
            "bathing_soap": "M",
            "sanitary": "-",
            "diapers": "farmer",
            "cooking_pot": "farmer",
            "plate": "farmer",
            "spoon": "farmer",
            "water": "farmer",
            "food": "farmer"
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

