function get_pronto_with_condition(url, is_filter) {
    var my_date_field = function(config) {
        jsGrid.Field.call(this, config);
    };

    my_date_field.prototype = new jsGrid.Field({
        sorter: function(date1, date2) {
            return new Date(date1) - new Date(date2);
        }
    });

    jsGrid.fields.date = my_date_field;

    $("#jsGrid").jsGrid({
        height: "720px",
        width: "2700px",
        filtering: is_filter,
        heading: true,
        editing: false,
        editButton: false,
        inserting: false,
        deleteButton: false,
        sorting: true,
        paging: true,
        autoload: true,
        pageSize: 15,
        pageButtonCount: 5,
        confirmDeleting: false,
        rowDoubleClick: function(args) {
             window.open('https://pronto.int.net.nokia.com/pronto/problemReport.html?prid=' + args["item"]["pronto_id"]);
         },
        controller: {
            loadData: function(filter) {
                return $.ajax({
                    type: "GET",
                    url: url,
                    data: filter,
                    dataType:"json"
                });
            }
        },
        fields: [
            { name:"pronto_id", title:"Pronto ID", type: "text" , width: "90px" },
            { name:"is_top", title:"Top", type: "text" , width: "50px" },
            { name:"release", title:"Release", type: "text", width:"125px"  },
            { name:"feature", title:"Feature", type: "text", width:"125px"  },
            { name:"title", title:"Title", type: "text", width:"610px" },
            { name:"build", title:"Build", type: "text", width:"250px" },
            { name:"severity", title:"Severity", type:"text", width:"100px" },
            { name:"responsible_person", title:"Responsible Person", type: "text", width:"150px"},
            { name:"status", title:"Status", type:"text", width:"100px" },
            { name:"transfer_from", title:"From Group", type:"text", width:"260px" },
            { name:"transfer_to", title:"To Group", type:"text", width:"260px" },
            { name:"rca_state", title:"RCA State", type:"text", width:"100px" },
            { name:"reported_date", title:"Report", type: "date" , width:"160px" },
            { name:"in_date", title:"In", type: "date", width:"160px" },
            { name:"out_date", title:"OUT", type: "date", width:"160px" },
            { name:"rft_date", title:"RFT", type: "date", width:"160px" },
            { name:"group_idx", title:"Group", type:"text", width:"260px" },
            { type: "control" }
        ]
    });
};

function chk(id,fieldName){
    $("#jsGrid").jsGrid("fieldOption", fieldName, "visible", $('#'+id).prop('checked'));
}