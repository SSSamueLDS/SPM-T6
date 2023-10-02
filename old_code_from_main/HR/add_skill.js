const app = Vue.createApp({
    data() {
        return {
            new_skill: "",
            success: false,
            error: false,
            success_msg: "",
            error_msg: "",
        }
    },
    computed:{
        check_input(){
            if(this.new_skill == "" || this.new_skill.length>50){
                return true;
            }
            else{
                return false;
            }
        }
    },
    methods: {
        add_skill(){
            //call API
            $(async() => {           
                // Change serviceURL to your own
                var serviceURL = "http://localhost:5003/add_skill";
    
                try {
                    const response =
                     await fetch(
                       serviceURL, { method: 'POST', body: JSON.stringify({"skill_name": this.new_skill}), headers: { 'Content-Type': 'application/json' } }
                    );
                    const result = await response.json();
                    if (response.status === 200) {
                        skill_added = result.data.skill_name
                        this.success = true;
                        this.success_msg = skill_added + " added successfully to the database.";
                        this.error = false;
                        this.error_msg = "";
                        this.new_skill = "";
                    }
                    if (response.status === 201) {
                        skill_added = result.data.skill_name
                        this.error = true;
                        this.error_msg = skill_added +" already exists in the database.";
                        this.success = false;
                        this.success_msg = "";
                    }
                }
                catch (error) {
                    this.error = true;
                    this.error_msg = "Error adding skill to the database.";
                }
            })
            new_skill = "";
        }
    },
    created(){
        
    }
});

app.mount('#app');