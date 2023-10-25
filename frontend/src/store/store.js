import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import axios from 'axios';

export default createStore({
    state: {
        staffAccessRole: null,
        isLoading : false,
        all_skills: [],
        all_dept: [],
        all_roles: [],
        all_listing: [],
        all_access_controls: [],
        user_skills: [],
        logged_in_staff: null
    },
    mutations: {
        setLoading(state, isLoading){
            state.isLoading = isLoading;
        },
        setStaffAccessRole(state, role) {
            state.staffAccessRole = role;
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
            state.user_skills = skills;
        },
        setAccessControls(state, data) {
            state.all_access_controls = data;
        },
        setLoggedinStaff(state, data) {
            state.logged_in_staff = data;
        },

        logout(state) {
            state.logged_in_staff = null;
            state.staffAccessRole = null;
            state.user_skills = [];
            // Clear other states if necessary
            localStorage.removeItem('vuex');
        },

        },
    plugins: [createPersistedState({
        paths: ['logged_in_staff', 'staffAccessRole', 'user_skills']}
        )],
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
        async fetchAccessControls({ commit }) {
            const response = await axios.get(`http://127.0.0.1:5004/access_control`);
            commit('setAccessControls', response.data.data);
        },
        async login({ commit, dispatch, state }, userID) {
            try {
              const response = await axios.get(`http://127.0.0.1:5004/staffs/${userID}`);
              if (response.data) {
                const user = response.data.data;
                if (!state.all_access_controls.length) {
                    await dispatch('fetchAccessControls');
                }
                const role = state.all_access_controls.find(r => r.access_id === user.role);
                if (role) {
                    console.log(role);
                    user.role = role.access_control_name;
                }
                commit('setLoggedinStaff', user);
                dispatch('fetchSkillsForUser', userID);
              } else {
                throw new Error('User not found');
              }
            } catch (error) {
                throw new Error(`Error during login: ${error.message}`);
            }
            
          },
        

    }
});
