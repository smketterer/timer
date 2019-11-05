<template>
  <div class="form list">
    <div class="date-controls">
      <el-button @click="addDays(-1)" type="default" icon="el-icon-arrow-left"></el-button>
      <el-date-picker @change="getTimeRecords()" v-model="date" type="date" placeholder="Date" :clearable="false"></el-date-picker>
      <el-button @click="addDays(1)" type="default" icon="el-icon-arrow-right"></el-button>
    </div>
    <div v-loading="loading" class="time-records">
      <div v-for="record in timeRecords">
        <el-card shadow="never">
          <span>
            <div>
              <el-button :loading="true" type="text" v-if="record.parent_type == 'Task' && tasksLoading">Loading</el-button>
              <el-button @click="openLink(getLinkToParent(record.parent_id, record.parent_type))" type="text" v-else-if="getProjectOrTaskById(record.parent_id, record.parent_type)">
                {{ getProjectOrTaskById(record.parent_id, record.parent_type)}}
              </el-button>
              <el-button class="el-button--text-disabled" type="text" v-else>Deleted</el-button>
            </div>
            <div>
              {{ record.summary }}
            </div>
          </span>
          <span>{{ formatTimes(record.value) }}</span>
          <div class="time-record--badges">
            <el-tag v-if="record.billable_status == 1" type="success" size="mini">Billable</el-tag>
            <el-tag type="info" size="mini">{{ getJobTypeById(record.job_type_id) }}</el-tag>
            <el-button type="plain" icon="el-icon-delete" size="mini" @click="deleteTimeRecord(record.url_path)"></el-button>
          </div>
          <div>
          </div>
        </el-card>
      </div>
      <el-row v-if="timeRecords.length" :gutter="6">
        <el-col :span="8">
          <div class="el-tag el-tag--primary el-tag--small">
            <i class="el-icon-time"></i> Total: {{ formatTimes(totalTime) }}
          </div>
        </el-col>
        <el-col :span="8">
          <div class="el-tag el-tag--primary el-tag--small">
            <i class="el-icon-time"></i> Billable: {{ formatTimes(totalBillableTime) }}
          </div>
        </el-col>
        <el-col :span="8">
          <div class="el-tag el-tag--primary el-tag--small">
            Efficiency: {{ Math.round((totalBillableTime / totalTime) * 100) }}%
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyTime',
  components: {},
  data: function() {
    return {
      date: new Date(),
      timeRecords: [],
      loading: false,
      projects: [],
      tasks: [],
      jobTypes: [],
      tasksLoading: false,
      url: ""
    }
  },
  computed: {
    totalTime: function() {
      let time = 0
      for (let timeRecord of this.timeRecords) {
        time += timeRecord.value
      }
      return time
    },
    totalBillableTime: function() {
      let time = 0
      for (let timeRecord of this.timeRecords) {
        if (timeRecord.billable_status == 1) {
          time += timeRecord.value
        }
      }
      return time
    }
  },
  mounted: function() {
    this.getTimeRecords()
    eel.get_url()((val) => {
      this.url = val
    })
    eel.get_projects()((val) => {
      this.projects = val
    })
    eel.get_job_types()((val) => {
      this.jobTypes = val
    })
    this.tasksLoading = true
    eel.get_tasks()((val) => {
      this.tasks = val
      this.tasksLoading = false
    })
  },
  methods: {
    addDays(days) {
      let result = new Date(this.date)
      result.setDate(result.getDate() + days)
      this.date = result
      this.getTimeRecords()
    },
    getTimeRecords() {
      this.loading = true
      this.timeRecords = []
      this.date.setMinutes(0);
      this.date.setSeconds(0);
      this.date.setMilliseconds(0);
      this.date.setHours(0);

      let offset = new Date().getTimezoneOffset() * 60

      eel.list_daily_time_records(this.date.getTime() / 1000, offset)((val) => {
        this.timeRecords = val
        this.loading = false
      })
    },
    deleteTimeRecord(url) {
      eel.delete(url)((val) => {
        this.getTimeRecords()
      })
    },
    getProjectOrTaskById(id, type) {
      // parent_id: 3
      // parent_type: "Project"
      // ... /projects/47/
      //
      // parent_id: 39260
      // parent_type: "Task"
      // ... /projects/47/tasks/39260
      if (type == "Project") {
        for (let project of this.projects) {
          if (project.id == id) {
            return project.name
          }
        }
      } else if (type == "Task") {
        for (let task of this.tasks) {
          if (task.id == id) {
            return task.name
          }
        }
      }
    },
    getLinkToParent(id, type) {
      if (type == "Project") {
        for (let project of this.projects) {
          if (project.id == id) {
            return project.url_path
          }
        }
      } else if (type == "Task") {
        for (let task of this.tasks) {
          if (task.id == id) {
            return task.url_path
          }
        }
      }
    },
    openLink(url) {
      window.open(`${ this.url }${ url }`, '_blank')
    },
    getJobTypeById(id) {
      for (let jobType of this.jobTypes) {
        if (jobType.id == id) {
          return jobType.name
        }
      }
    },
    formatTimes(time) {
      let formattedTime = (time.toFixed(2)).split(".");
      let minutes = String(Math.round(formattedTime[1] / 10 * 6))
      if (minutes.length == 1) {
        minutes = `${ minutes }0`
      }
      return `${ formattedTime[0] }:${ minutes }`
    }
  }
}
</script>
