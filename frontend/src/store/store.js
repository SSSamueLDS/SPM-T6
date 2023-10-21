import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
    state: {
        staffAccessRole: null,
        staffSkills: [],
        isLoading : false,
        all_skills: [],
        all_dept: [],
        all_roles: [],
        all_listing: [],
        country: null,
        dept: null,
        email: null,
        role: null,
        staff_fname: null,
        staff_id: null,
        staff_lname: null,
        userID: null,
        
    },
    getters: {
        isLoggedIn: state => !!state.loggedInStaff,
        // ... other getters
    },
    mutations: {
        setLoading(state, isLoading){
            state.isLoading = isLoading;
        },
        setStaffAccessRole(state, role) {
            state.staffAccessRole = role;
        },
        setStaffSkills(state, skills) {
            state.staffSkills = skills;
        },
        setAllSkills(state, data) {
            state.all_skills = data;
        },
        setAllDept(state, data) {
            state.all_dept = data;
        },
        setAllRoles(state, data) {
            state.all_roles = data;
        },
        setAllListing(state, data) {
            state.all_listing = data;
        },
        setUserSkills(state, skills) {
            state.userSkills = skills;
        },
        setLoggedinStaff(state, staffData) {
            state.country = staffData.country;
            state.dept = staffData.dept;
            state.email = staffData.email;
            state.role = staffData.role;
            state.staff_fname = staffData.staff_fname;
            state.staff_id = staffData.staff_id;
            state.staff_lname = staffData.staff_lname;
            // ... set other state properties if needed ...
        },

        logout(state) {
            state.loggedInStaff = null;
            state.staffAccessRole = null;
            state.staffSkills = [];
            // Clear other states if necessary
        },

        },

    actions: {
        async fetchAllSkills({ commit }) {
            const response = await axios.get('http://127.0.0.1:5003/skills');
            commit('setAllSkills', response.data.data);
        },
        async fetchAllDept({ commit }) {
            const response = await axios.get('http://127.0.0.1:5004/staffs/dept');
            commit('setAllDept', response.data.data);
        },
        async fetchAllRoles({ commit }) {
            const response = await axios.get('http://127.0.0.1:5005/roles');
            commit('setAllRoles', response.data.data);
        },
        async fetchAllListing({ commit }) {
            const response = await axios.get('http://127.0.0.1:5002/listings');
            commit('setAllListing', response.data.data);
        },
        async fetchSkillsForUser({ commit }, userID) {
            const response = await axios.get(`http://127.0.0.1:5004/staffs/skills/${userID}`);
            commit('setUserSkills', response.data.data);
        },
        async login({ commit }, userID) {
            try {
              const response = await axios.get(`http://127.0.0.1:5004/staffs/${userID}`);
              if (response.data) {
                console.log(response.data.data);
                commit('setLoggedinStaff', response.data.data);

                // dispatch('fetchStaffSkills', userID);
                // dispatch other actions as needed...
              } else {
                alert('User not found');
              }
            } catch (error) {
              alert('Error during login:', error.message);
            }
          },
        

    }
});
