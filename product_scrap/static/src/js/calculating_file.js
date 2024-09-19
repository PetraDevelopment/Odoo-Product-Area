// $(document).ready(function(){
//     console.log('sssssssssssssssssssssssssssssssssssssssssssss')
//     var button1=$('.but-cal');
//     console.log(button1.val(),'11111111')

//     button1.on('click', function () {
//         alert('heloooooooo');
//     });

//     // button1.click(function(){
//     //     alert('heloooooooo');
//     //     var line_id = this.id;  // Pass the ID of the sale order line here
//     //     $.ajax({
//     //         url: '/calculate_product_qty_sales',
//     //         // type: 'POST',
//     //         dataType: 'json',
//     //         data: {
//     //             'line_id': line_id,
//     //         },
//     //         success: function(response){
//     //             if (response.result === 'success') {
//     //                 var total = response.total;
//     //                 console.log('Product quantity calculated successfully: ' + total);
//     //                 // Do something with the calculated total
//     //             } else {
//     //                 console.error('Error: ' + response.message);
//     //                 // Handle error
//     //             }
//     //         },
//     //         error: function(xhr, errmsg, err){
//     //             console.log(xhr.status + ": " + xhr.responseText);
//     //         }
//     //     });
//     // });

//     var button2=$('[name="calculate_uom_and_total_sales"]');
//     button2.click(function()
//     {
//         var line_id = this.id;  // Pass the ID of the sale order line here
//         $.ajax({
//             url: '/calculate_uom_and_total_sales',
//             type: 'POST',
//             dataType: 'json',
//             data: {
//                 'line_id': line_id,
//             },
//             success: function(response){
//                 if (response.result === 'success') {
//                     var totalQuantity = response.total_quantity;
//                     console.log('UOM and total calculated successfully: ' + totalQuantity);
//                     // Do something with the calculated total quantity
//                 } else {
//                     console.error('Error: ' + response.message);
//                     // Handle error
//                 }
//             },
//             error: function(xhr, errmsg, err){
//                 console.log(xhr.status + ": " + xhr.responseText);
//             }
//         });
//     });
// });



/////////////////////////done step/////////////////
// odoo.define('product_scrap.print_product_names', function (require) {
//     "use strict";

//     var Widget = require('web.Widget');
//     var rpc = require('web.rpc');

//     var PrintProductNamesWidget = Widget.extend({
//         start: function () {
//             var self = this;
//             rpc.query({
//                 model: 'sale.order.line',
//                 method: 'search_read',
//                 domain: [],
//                 fields: ['product_id'],
//             }).then(function (lines) {
//                 self.printProductNames(lines);
//             });
//         },

//         printProductNames: function (lines) {
//             console.log('Product Names:');
//             for (var i = 0; i < lines.length; i++) {
//                 console.log(lines[i].product_id[1]); // Assuming product_id is a many2one field
//             }
//         },
//     });

//     new PrintProductNamesWidget(null).appendTo(document.body);

//     return PrintProductNamesWidget;
// });


////////////////////////

// odoo.define('product_scrap.print_product_names', function (require) {
//     "use strict";

//     var Widget = require('web.Widget');
//     var rpc = require('web.rpc');

//     var PrintProductNamesWidget = Widget.extend({
//         start: function () {
//             var self = this;
//             rpc.query({
//                 model: 'sale.order.line',
//                 method: 'search_read',
//                 domain: [],
//                 fields: ['product_id','product_uom_qty'],
//             }).then(function (lines) {
//                 self.printProductNames(lines);
//             });
//         },

//         printProductNames: function (lines) {
//             console.log('Product Names:');
//             for (var i = 0; i < lines.length; i++) {
//                 console.log(lines[i].product_id[1],lines[i].product_uom_qty); // Assuming product_id is a many2one field
//             }
//         },
//     });

//     new PrintProductNamesWidget(null).appendTo(document.body);

//     return PrintProductNamesWidget;
// });



// odoo.define('product_scrap.print_product_names', function (require) {
//     "use strict";

//     var rpc = require('web.rpc');

//     // Define your module logic
//     var PrintProductNames = {
//         fetchRecords: function () {
//             var model = 'res.partner';
//             var domain = [];
//             var fields = [];
            
//             rpc.query({
//                 model: model,
//                 method: 'search_read',
//                 args: [domain, fields],
//             }).then(function (data) {
//                 console.log(data);
//             });
//         }
//     };

//     // Call the fetchRecords function when the module is loaded
//     PrintProductNames.fetchRecords();

//     // Optionally, return any functions or variables that you want to make accessible outside of the module
//     return PrintProductNames;
// });


odoo.define('product_scrap.calculating_file', function (require) {
    'use strict';

    var rpc = require('web.rpc');

    $(document).ready(function () {
        $('.but-cal[name="calculate_product_qty_sales"]').on('click', function () {
            rpc.query({
                model: 'sale.order',
                method: 'calculate_product_qty_sales',
                args: [],
            }).then(function (result) {
                // Handle the result if needed
            });
        });
    });
});

