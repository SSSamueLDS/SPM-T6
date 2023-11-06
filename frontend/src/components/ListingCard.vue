<template>
    <div class="row mt-3">
        <div class="mx-2">
            <!-- Card for each role -->
            <div class="card rounded-4" style="cursor: pointer">
                <div class="card-body" style="text-align: left">
                    <h5 class="card-title fw-bold" >Listing #{{ listing.listing_id }}: {{ listing.listing_name }}</h5>

                    <p class="card-text">Skill Match: {{ skillMatchPercentage(listing.skill_ids) }}%</p>
                    <p class="card-text">{{ truncateDescription(listing.listing_description) }}</p>

                    <!-- Skills Display -->
                    <p class="card-text">
                        Skill Required:
                        <span v-for="(skillName, index) in listing.skill_names" :key="index">
                            <span 
                                :style="{ 
                                    backgroundColor: userHasSkill(listing.skill_ids[index]) ? 'greenyellow' : 'lightgray', 
                                    borderRadius: '5px', 
                                    fontWeight: '600',
                                    padding: '5px', 
                                    marginRight: '5px', 
                                    marginBottom: '5px', 
                                    display: 'inline-block'
                                }"
                            >
                                {{ skillName }}
                            </span>
                        </span>
                    </p>


                    <p class="card-text">Department: {{ listing.dept }}</p>
                    <p class="card-text"><small class="text-muted">Deadline: {{ listing.deadline }}</small></p>

                    <!-- Action Buttons -->
                    <div class="d-flex justify-content-end">
                        <button class="btn mx-2" 
                                style="color: black; background-color: greenyellow; font-weight: bold"
                                v-bind:data-bs-toggle="'modal'"
                                v-bind:data-bs-target="'#' + listing.listing_tag + 'Modal'">
                            View Details
                        </button>
                        <button href="#" class="btn btn-dark" 
                                style="color: greenyellow; font-weight: bold"
                                @click="applyForListing(listing.listing_id)">
                            Apply
                        </button>
                    </div>
                </div>
            </div>

            <!-- Listing description modal -->
            <div class="modal fade" :id="listing.listing_tag + 'Modal'" tabindex="-1" :aria-labelledby="listing.listing_tag" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" :id="listing.listing_tag">{{ listing.listing_name }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-start">
                            <p class="fw-bold">Application Deadline: {{ listing.deadline }}</p>
                            <p>Required Skills: {{ listing.skill_names.join(", ") }}</p>
                            <p class="fw-bold">About the listing</p>
                            <p>{{ listing.listing_description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ListingCard",
    props: {
        listing: {
            type: Object,
            required: true
        },
        userSkills: {
            type: Array,
            required: true
        },
        skillMatchPercentage: {
            type: Function,
            required: true
        },
        truncateDescription: {
            type: Function,
            required: true
        },
        userHasSkill: {
            type: Function,
            required: true
        },
        applyForListing: {
            type: Function,
            required: true
        }
    }
}
</script>
