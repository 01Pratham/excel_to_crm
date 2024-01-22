function UpdateHTML( obj ){
    $("." + obj.phase.replace(/ /, '')).each(function () {
        if ($(this).hasClass(obj.group.replace(/ /, '')) && $(this).hasClass("Quantity") ) {
            if ($(this).prop("id") == "prod_"+ obj.prod_id) {
              var val = parseInt( obj.product_qty );
              if (val == 0){
                $(this).html('');
              }else{
                $(this).html(val);
              }
            }
        }
        // if ($(this).hasClass(obj.group.replace(/ /, '')) && $(this).hasClass("Discount") ) {
        //     if ($(this).prop("id") == "prod_"+ obj.prod_id) {
        //       var val = parseFloat(obj.product_qty);
        //       if (val == 0){
        //         $(this).html('');
        //       }else{
        //         $(this).html(val.toFixed(2));
        //       }
        //     }
        // }
    });
} 