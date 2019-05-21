<template>
  <div class="form">
    Reports
  </div>
</template>

<script>
export default {
  name: 'Reports',
  components: {},
  data: function() {
    return {
      date: new Date(),
    }
  },
  computed: {
    // totalTime: function() {
    //   let time = 0
    //   for (let timeRecord of this.timeRecords) {
    //     time += timeRecord.value
    //   }
    //   return time
    // },
    // totalBillableTime: function() {
    //   let time = 0
    //   for (let timeRecord of this.timeRecords) {
    //     if (timeRecord.billable_status == 1) {
    //       time += timeRecord.value
    //     }
    //   }
    //   return time
    // }
  },
  mounted: function() {
    // this.getTimeRecords()
    // eel.get_url()((val) => {
    //   this.url = val
    // })
    // eel.get_projects()((val) => {
    //   this.projects = val
    // })
    // eel.get_job_types()((val) => {
    //   this.jobTypes = val
    // })
    // this.tasksLoading = true
    // eel.get_tasks()((val) => {
    //   this.tasks = val
    //   this.tasksLoading = false
    // })
  },
  methods: {

  }
}
</script>
