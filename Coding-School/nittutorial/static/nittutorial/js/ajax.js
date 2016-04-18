$(document).ready(function(){
    $('#mysearch').click(function() {
        //alert($('#search-text').val());
        $.ajax({
            type: "POST",
            url: "/search/",
            data: { 
                'search-text' : $('#search-text').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html',
            
        });
        
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data);
}