<template>
    <nav aria-label="Employee page navigation">
      <ul class="pagination">
        <li class="page-item">
          <a class="page-link text-black" @click="go_previous_page()">Previous</a>
        </li>
        <li class="page-item" v-for="pageNumber in visiblePageRange" :key="pageNumber">
          <a class="page-link text-black" @click="go_page(pageNumber)" :class="{ 'active-page': pageNumber === currentPage }">{{ pageNumber + 1 }}</a>
        </li>
        <li class="page-item">
          <a class="page-link text-black" @click="go_next_page()">Next</a>
        </li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    props: {
      totalPages: {
        type: Number,
        required: true,
      },
      currentPage: {
        type: Number,
        default: 0,
      },
    },
    data() {
      return {
        maxVisiblePages: 5,
      };
    },
    computed: {
      visiblePageRange() {
        let startPage = Math.max(this.currentPage - Math.floor(this.maxVisiblePages / 2), 0);
        let endPage = startPage + this.maxVisiblePages - 1;

        if (endPage >= this.totalPages) {
            endPage = this.totalPages - 1;
            startPage = Math.max(endPage - this.maxVisiblePages + 1, 0);
        }
        return Array.from({ length: (endPage - startPage) + 1 }, (_, i) => startPage + i);
      },
    },
    methods: {
      go_previous_page() {
        if (this.currentPage > 0) this.$emit('update:currentPage', this.currentPage - 1);
      },
      go_next_page() {
        if (this.currentPage < this.totalPages - 1) this.$emit('update:currentPage', this.currentPage + 1);
      },
      go_page(pageNumber) {
        this.$emit('update:currentPage', pageNumber);
      },
    },
  };
  </script>
  
  <style scoped>
    .active-page a {
      background-color: #007bff !important;
      color: white !important;
    }
  </style>
  