// This is to handle for edit role funtion 

$(document).ready(function(){
    $("#submitButton").click(function(event){
        console.log("Button clicked")
        event.preventDefault();
        let roleData = {
            role_name: $("#role_name").val(),
            role_description: $("#role_description").val(),
            deadline: $("#deadline").val()
        };

        axios.post('http://0.0.0.0:5002/create_role', roleData)
            .then(function (response) {
                alert('Role created successfully!');
                // Here, you can also close the modal or refresh the page
                // $("#createRoleModal").modal('hide');
            })
            .catch(function (error) {
                alert('Failed to create the role. Please try again.');
            });
    });
});