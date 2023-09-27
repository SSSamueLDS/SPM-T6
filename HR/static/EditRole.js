$(document).ready(function() {
    // Get the role ID from the URL or some other source
    let roleID = ;

    // Fetch the existing data for the role
    axios.get(`http://0.0.0.0:5002/roles/${roleID}`)
        .then(function(response) {
            let role = response.data;
            // Prepopulate the form with the existing data
            $("#role_name").val(role.role_name);
            $("#role_description").val(role.role_description);
            $("#deadline").val(role.deadline);
        })
        .catch(function(error) {
            console.error('Failed to fetch the role data:', error);
        });

    $("#submitButton").click(function(event) {
        console.log("Button clicked");
        event.preventDefault();
        let roleData = {
            role_name: $("#role_name").val(),
            role_description: $("#role_description").val(),
            deadline: $("#deadline").val()
        };

        // Send a PUT request to update the role
        axios.put(`http://0.0.0.0:5002/update_role/${roleID}`, roleData)
            .then(function(response) {
                alert('Role updated successfully!');
                // Here, you can also close the modal or refresh the page
                // $("#createRoleModal").modal('hide');
            })
            .catch(function(error) {
                alert('Failed to update the role. Please try again.');
            });
    });
});
