import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { AdminDashboard } from './pages/admin/Dashboard'
import { AdminCourses } from './pages/admin/Courses'
import { AdminCourseDetail } from './pages/admin/CourseDetail'
import { AdminStaging } from './pages/admin/Staging'
import { StudentDashboard } from './pages/student/Dashboard'
import { StudentCourse } from './pages/student/Course'
import { StudentConcept } from './pages/student/Concept'
import { StudentAssessment } from './pages/student/Assessment'
import { RoleSelect } from './pages/RoleSelect'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RoleSelect />} />
        <Route path="/admin" element={<Layout role="admin" />}>
          <Route index element={<AdminDashboard />} />
          <Route path="courses" element={<AdminCourses />} />
          <Route path="courses/:courseId" element={<AdminCourseDetail />} />
          <Route path="staging" element={<AdminStaging />} />
        </Route>
        <Route path="/student" element={<Layout role="student" />}>
          <Route index element={<StudentDashboard />} />
          <Route path="courses/:courseId" element={<StudentCourse />} />
          <Route path="courses/:courseId/units/:unitId" element={<StudentConcept />} />
          <Route path="courses/:courseId/units/:unitId/assessment" element={<StudentAssessment />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
