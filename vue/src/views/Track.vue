<template>
  <div class="form track">
    <el-select clearable filterable v-model="project" @change="getTasks()" placeholder="Project">
      <el-option v-for="item in projectOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
    </el-select>
    <el-select clearable filterable v-if="this.project" v-model="task" placeholder="Tasks">
      <el-option v-for="item in taskOptions.tasks" :key="item.id" :label="item.name" :value="item.id">
        <span class="task-name">{{ item.name }}</span>
        <div class="task-controls">
          <el-button icon="el-icon-more" @click="openLink(item.url_path)" size="mini"></el-button>
        </div>
      </el-option>
    </el-select>
    <el-select clearable filterable v-model="jobType" placeholder="Job Type">
      <el-option v-for="item in jobTypeOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
    </el-select>
    <div class="times">
      <el-date-picker v-model="date" type="date" placeholder="Date" :clearable="false"></el-date-picker>
      <el-input clearable placeholder="Time" v-model="time"></el-input>
    </div>
    <el-checkbox v-model="billable">Billable</el-checkbox>
    <el-checkbox v-if="this.task" v-model="markCompleted">Complete</el-checkbox>
    <el-input clearable placeholder="Summary" type="textarea" rows="5" v-model="summary"></el-input>
    <el-button :loading="this.sending" :disabled="!this.project || !this.jobType || !this.time || !this.date" @click="createTimeRecord()" type="primary">
      <span v-if="!this.sending">Save</span>
      <span v-else>Saving</span>
    </el-button>
  </div>
</template>

<script>
export default {
  name: 'Track',
  components: {},
  data: function() {
    return {
      project: "",
      projectOptions: [{}],
      task: "",
      taskOptions: [{}],
      jobType: "",
      jobTypeOptions: [{}],
      date: new Date(),
      time: "",
      summary: "",
      billable: false,
      markCompleted: false,
      sending: false,
      url: ""
    }
  },
  mounted: function() {
    eel.get_projects()((val) => {
      this.projectOptions = val
    })
    eel.get_job_types()((val) => {
      this.jobTypeOptions = val
    })
    eel.get_url()((val) => {
      this.url = val
    })
  },
  methods: {
    getTasks() {
      this.task = ""
      eel.get_tasks_by_project(this.project)((val) => {
        this.taskOptions = val
      })
    },
    openLink(url) {
      window.open(`${ this.url }${ url }`, '_blank')
    },
    createTimeRecord() {
      // Start the loading button.
      this.sending = true
      // Strip out all the time information so it shows up on the right day.
      this.date.setMinutes(0);
      this.date.setSeconds(0);
      this.date.setMilliseconds(0);
      this.date.setHours(0);
      // Convert billable bool to 0/1.
      let billable = 0
      if (this.billable == true) {
        billable = 1
      }
      // Convert time from string to value.
      let timeValue = 0
      if (this.time.indexOf(":") !== -1) {
        // Hours and minutes
        let timeString = this.time.split(":")
        let hours = 0
        let minutes = 0
        if (timeString[0] == '') {
          timeString[0] = 0
        }
        if (timeString[0]) {
          hours = parseInt(timeString[0])
        }
        if (timeString[1]) {
          minutes = parseInt(timeString[1])
        }
        timeValue = hours + (minutes / 60)
      } else {
        // Hours
        timeValue = this.time
      }
      eel.create_time_record(this.project, this.task, this.jobType, this.date, timeValue, billable, this.summary)((val) => {
        // Check response to make sure it's the proper response.
        this.sending = false
        this.project = ""
        this.task = ""
        this.jobType = ""
        this.time = ""
        this.billable = false
        this.summary = ""
      })
      if (this.markCompleted) {
        // Mark the task as complete.
        eel.complete_task(this.task)((val) => {
          // console.log(val)
        })
      }
    }
  }
}
</script>
