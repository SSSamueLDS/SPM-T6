const app = Vue.createApp({
    data() {
        return {
            skills: [],
            grouped_skills: [],
            database_error: false,
            current_page:1
        }
    },
    computed:{
        
    },
    methods: {
        sort_alphabetically(){
            this.skills = this.skills.sort((a,b) => (a.skill_name > b.skill_name) ? 1 : ((b.skill_name > a.skill_name) ? -1 : 0));
            this.grouped_skills = this.group_skills();
            this.current_page = 1;
        },
        sort_by_ID(){
            this.skills = this.skills.sort((a,b) => (a.skill_ID > b.skill_ID) ? 1 : ((b.skill_ID > a.skill_ID ? -1 : 0)));
            this.grouped_skills = this.group_skills();
            this.current_page = 1;
        },
        //group skills in groups of 10, for display purposes
        //remainder in the last group
        group_skills(){
            var grouped_skills = [];
            var group = [];
            var i = 0;
            for (i = 0; i < this.skills.length; i++){
                if(i % 10 == 0 && i != 0){
                    grouped_skills.push(group);
                    group = [];
                }
                group.push(this.skills[i]);
            }
            grouped_skills.push(group);
            console.log(grouped_skills);
            return grouped_skills;
        },
        go_page(i){
            this.current_page = i;
        },
        go_previous_page(){
            if(this.current_page >1){
                this.current_page--;
            }
        },
        go_next_page(){
            if(this.current_page < this.grouped_skills.length-1){
                this.current_page++;
            }
        }
    },
    created(){
        //Call to fetch skill data from API
        $(async() => {           
            // Change serviceURL to your own
            var serviceURL = "http://localhost:5003/skills";

            try {
                const response =
                 await fetch(
                   serviceURL, { method: 'GET'}
                );
                const result = await response.json();
                 if (response.status === 200) {
                    // success case
                    var skills = result.data; //array of skill objects
                    this.skills = skills;

                    //group skills in groups of 10, for display purposes
                    var grouped_skills = [];
                    var group = [];
                    var i = 0;
                    for (i = 0; i < this.skills.length; i++){
                        if(i % 10 == 0 && i != 0){
                            grouped_skills.push(group);
                            group = [];
                        }
                        group.push(this.skills[i]);
                    }
                    grouped_skills.push(group);
                    this.grouped_skills = grouped_skills;
                }
            }
            catch (error) {
                this.database_error = true;
            }
        })
    }
});

app.mount('#app');