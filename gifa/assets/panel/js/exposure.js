// Jquery Listener
$(document).ready(function () {
	// Initiate the data table
    $('#exposure').DataTable({
    	responsive: true,
    	select: true,
    	dom: 'Bfrtip',
        processing: true,
        buttons: [
            'copy', 'csv', 'excel', 'pdf'
        ],
        ajax: {
  	      url: '//' + window.location.hostname + ':8000/dashboard/bangunanosm'
        },
    	columns	: [
    		{data: "nama"},
            {data: "jenis_bangunan"},
            {data: "exposure_index"},
            {data: "flood_depth"},
    	],
        order: [[0, "desc"]],
        // function to change background cell color based on specific value
        createdRow: function(row, data, index) {
            if(data["exposure_index"] <= 30) {
                $('td', row).eq(2).css('background-color', '#fafa46');
                $('td', row).eq(2).addClass('exposure');
            } else if(data["exposure_index"] > 30 || data["exposure_index"] <= 60)  {
                $('td', row).eq(2).css('background-color', '#eb9234');
                $('td', row).eq(2).addClass('exposure');
            } else if (data["exposure_index"] >= 60)  {
                $('td', row).eq(2).css('background-color', '#ff1212');
                $('td', row).eq(2).addClass('exposure');
            }
        }
    });
});



