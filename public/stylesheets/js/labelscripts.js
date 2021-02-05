$(document).ready(function () {       
    // load image-picker
    $('.image-picker').imagepicker({
        hide_select:  true, 
    });
    $("#label_run_id").hide()

    //ShortClick Description Labels
    $('label[id^="fastclicklabel_"').click(function(){
        var labelname =  $(this).text()
        $('#search').val($('#search').val() + labelname)
        UpdateTable()
    });

    //ShortClick Colors
    $('div[id^="color_id_"').click(function(){
        title_split = $(this).attr('title').split("(")
        var colorid =  title_split[1].replace(")","")
        var colorname = title_split[0]
        $('#input_colorid').val(colorid);
        $('#search').val( $('#search').val() + colorname)
        if($('#input_partno').val() != '') {
            var url = "//img.bricklink.com/P/" + colorid + "/" + $('#input_partno').val() + ".jpg";
        } 
        $('#img_foundpart').prop('src',url );   
        UpdateTable()
    });
   

    // Search https://stackoverflow.com/questions/9127498/how-to-perform-a-real-time-search-and-filter-on-a-html-table
    var $rows = $('#Parttable tr');
    $('#search').keyup(debounce(function() {
        UpdateTable()
    }, 300));

    
    function UpdateTable() {
        /*var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
        $rows.show().filter(function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();
        */
        var val = '^(?=.*\\b' + $.trim($('#search').val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
        reg = RegExp(val, 'i'),
        text;

        $rows.show().filter(function() {
            text =  $(this).text().replace(/\s+/g, ' ');
            return !reg.test(text);
        }).hide();
    }

 
     //Click on Parttable
     $('#Parttable').on('click', 'tr', function() {
         var values = $(this).find('td').map(function() {
             return $(this).text();
         });

         var url = "//img.bricklink.com/P/" + values[1] + "/" + values[2] + ".jpg"; 
         $('#img_foundpart').prop('src',url );   
         $('#input_colorid').val(values[1]);
         $('#input_partno').val(values[2]);
         $('#label_partname').text(values[3]);

     });

    //Click on label_predictedpartname
    $('#label_predictedpartname').on('click',function () {
        predicted_partno = $(this).text()
        var url = "//img.bricklink.com/PL/" + $(this).text() + ".jpg"; 
        $('#img_foundpart').prop('src',url );  
        $('#search').val( $('#search').val() + predicted_partno + " ") 
        $('#input_partno').val(predicted_partno);
        UpdateTable()

    });



     /** Binds a click event on a group title/label of a group. And then selects/deselects all the thumbnails of that group. */
    $('.group_title').on('click', function () {
        var optGroupLabel = $(this).html();
        var optGroup = $('*[label="' + optGroupLabel + '"]')
        var optGroupOptions = optGroup.find($('option'));
        var optGroupSelected = optGroup.data('selected');

        //Check if the optgroup is selected. 
        if (optGroupSelected) {
            //If true, then set the data-attribute selected to false and select all images under that option.
            optGroup.data('selected', false);
            optGroupOptions.prop("selected", false);
            
        } else {
            //if false, then set the data-attribute selected to true and deselect all images under that option.
            optGroup.data('selected', true);
            optGroupOptions.prop("selected", true);
            predict();
            
        }
        
        //This triggers the image picker to check for changes and update the images accordingly
        $('.image-picker').data('picker').sync_picker_with_select();
    });
 

     // Button label
     $("#button_label").on('click', function(){
         var sel = $("select").val();
         if(sel.length > 0  && $('#input_partno').val() != '') {
             $.post('/recognisedpart',   // url
                 {PartidsAndImageIds:  sel , 
                     Partno : $("#input_partno").val(),
                     Run_id :  $("#label_run_id").text(),
                     Color_id : $('#input_colorid').val(),
                     Identifier : "human",
                     Score : 100.0
                 }, // data to be submit
                 function(data, status, jqXHR) {// success callback
                         //refresh datapicker                            
 
                     }).done(function() {
                         var partid = sel[0].split("-")[0];
                         console.log("hide Partid " + partid )
                         $('#input_colorid').val('');
                         $('#input_partno').val('');
                         $('#label_partname').text("");
                         $('#search').val("");
                         $('div[class^="thumbnail '+ partid + '-"').hide();
                        // $("div.thumbnail.selected").hide()
                         $("select").val('');
                         var url = "https://img.brickowl.com/files/image_cache/large/placeholder.png"; 
                         $('#img_foundpart').prop('src',url );  
                     });
         } else
         alert("No images selected or no Partno given!")
     });

     
     // Button delete
     $("#button_deletePartimages").on('click',function(){
        var sel = $("select").val();
        if(sel.length > 0)  {
            $.post('/partimage/delete',   // url
                {ImageIds:  sel
                }, // data to be submit
                function(data, status, jqXHR) {// success callback
                        //refresh datapicker 
                    }).done(function() {
                        $("div.thumbnail.selected").hide()
                        $("select").val('');
                    });
        } else
        alert("No images selected to delete")
    });

        // Button delete
    $("#button_deleteSearchInput").on('click',function(){
        $('#search').val("");
        $('#input_colorid').val('');
        UpdateTable()
    });
    

    
     // Button Predict
     $("#button_predict").on('click',function(){
       predict();
    });
    //var selectmode = 0;
    // delete x button
  /*  $(document).on('keyup', function(key) { 
        console.log("key pressed: " + key.keyCode );
        var edit = 0;
        if (key.keyCode === 88) {
            edit = 1;           
            $('div').hover(function(){
                if(edit == 1) {
                    $(this).hide(); // if hovered then it has class active
                edit = 0;
                }

            });
        }
      
        if (key.keyCode === 16) {
            if(selectmode == 0) {
                console.log("select mode ON")
                selectmode = 1;
            } else {
                console.log("select mode OFF")
                selectmode = 0;
            }
            if(selectmode == 1) {
                $(document).on('mouseover', 'div.thumbnail', function(e) {
                    console.log($(e.target).attr('class'));
                  //  $(e.target).attr('class').val('div.thumbnail.selected')
                });
            }
        }
    });
*/


    function predict() {
       
        var imagepathtoPredicit = $("img.image_picker_image." + $("select").val()[0]).attr('src')
        console.log("predicting " + imagepathtoPredicit);

        if($("select").val().length > 0)  {
            $.post('/predict',   // url
                {imagepath: imagepathtoPredicit
                }, // data to be submit
                function(data, status, jqXHR) {// success callback
                        //refresh datapicker                            
                        $('#label_predictedpartname').text(data.predict_partno);    
                        var url = "//img.bricklink.com/PL/" + data.predict_partno + ".jpg"; 
                        $('#img_predictedpart').prop('src',url );     
                    }).done(function() {
                        //$("div.thumbnail.selected").hide()
                        //$("select").val('');

                    });
        } else
        alert("No images selected to delete")
    }

     function debounce(func, wait, immediate) {
         var timeout;
         return function() {
             var context = this, args = arguments;
             var later = function() {
                 timeout = null;
                 if (!immediate) func.apply(context, args);
             };
             var callNow = immediate && !timeout;
             clearTimeout(timeout);
             timeout = setTimeout(later, wait);
             if (callNow) func.apply(context, args);
         };
     };
 });
 
 