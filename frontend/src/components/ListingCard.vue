<template>
    <div class="row mt-3">
        <div class="mx-2">
            <!-- Card for each role -->
            <div class="card rounded-4" style="cursor: pointer">
                <div class="card-body">
                    <h5 class="card-title">Listing #{{  listing.listing_id }}: {{ listing.listing_name }}</h5>
                    <p class="card-text">
                        Skill Match: {{ skillMatchPercentage(listing.skill_ids) }}%
                    </p>
                    <p class="card-text">{{ truncateDescription(listing.listing_description) }}</p>
                    <p class="card-text">
                        Skill Required:
                        <span v-for="(skillName, index) in listing.skill_names" :key="index">
                            <span :style="{ backgroundColor: userHasSkill(listing.skill_ids[index]) ? 'yellow' : 'grey', borderRadius: '5px', padding: '5px', marginRight: '5px' }">
                                {{ skillName }}
                            </span>
                        </span>
                    </p>
                    <p class="card-text">
                        Department: {{ listing.dept }}
                    </p>
                    <p class="card-text">
                        <small class="text-muted">
                            Deadline: {{ listing.deadline }}
                        </small>
                    </p>
                    <div class="col" style="text-align: right">
                        <!-- Button to view details, which triggers the modal -->
                        <button
                            class="btn btn-info"
                            v-bind:data-bs-toggle="'modal'"
                            v-bind:data-bs-target="'#' + listing.listing_tag + 'Modal'">
                            View Details
                        </button>
                        <!-- Button to apply -->
                        <button
                            href="#"
                            class="btn btn-dark"
                            style="color: greenyellow; font-weight: bold"
                            @click="applyForListing(listing.listing_id)"
                        >
                            Apply
                        </button>
                    </div>
                </div>
            </div>
            
            <!--Listing description modal-->
            <div class="modal fade" :id="listing.listing_tag + 'Modal'" tabindex="-1" :aria-labelledby="listing.listing_tag" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" :id="listing.listing_tag">
                                {{ listing.listing_name }}
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" style="text-align: left">
                            <p style="font-weight: bold">
                                Application Deadline: {{ listing.deadline }}
                            </p>
                            <p>Required Skills: {{ listing.skill_names.join(", ") }}</p>
                            <p style="font-weight: bold">About the listing</p>
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
    },
    methods: {
    }
}
</script>
