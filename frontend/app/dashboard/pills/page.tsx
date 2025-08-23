"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Calendar } from "@/components/ui/calendar"
import { Pill, Plus, Clock, CheckCircle, AlertCircle, Package, TrendingUp, Edit, Trash2, Users } from "lucide-react"
import { HealthDashboardNav } from "@/components/health-dashboard-nav"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/contexts/AuthContext"
import { notificationService, PillReminder } from "@/services/notificationService"

interface Medication extends PillReminder {
  adherence: number
  nextDose: string
  color: string
  taken: boolean
}

export default function PillReminderPage() {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date())
  const [isAddingMedication, setIsAddingMedication] = useState(false)
  const [medications, setMedications] = useState<Medication[]>([])
  const [newMedication, setNewMedication] = useState({
    name: "",
    dosage: "",
    frequency: "",
    times: "",
    stock: "",
    notes: "",
    caregiverNotify: false,
  })
  const { toast } = useToast()
  const { user } = useAuth()

  useEffect(() => {
    if (user) {
      // Initialize notification service
      notificationService.initialize(user.uid);
      
      // Load medications from Firebase
      loadMedications();
      
      // Subscribe to real-time updates
      const unsubscribe = notificationService.subscribeToReminders(user.uid, (reminders) => {
        const medicationsWithExtras = reminders.map(reminder => ({
          ...reminder,
          adherence: Math.floor(Math.random() * 100),
          nextDose: "2:00 PM",
          color: `hsl(${Math.random() * 360}, 70%, 50%)`,
          taken: false,
        }));
        setMedications(medicationsWithExtras);
      });

      return () => {
        unsubscribe();
        notificationService.cleanup();
      };
    }
  }, [user]);

  const loadMedications = async () => {
    if (!user) return;
    
    try {
      const reminders = await notificationService.getPillReminders(user.uid);
      const medicationsWithExtras = reminders.map(reminder => ({
        ...reminder,
        adherence: Math.floor(Math.random() * 100),
        nextDose: "2:00 PM",
        color: `hsl(${Math.random() * 360}, 70%, 50%)`,
        taken: false,
      }));
      setMedications(medicationsWithExtras);
    } catch (error) {
      console.error('Error loading medications:', error);
      toast({
        title: "Error",
        description: "Failed to load medications",
        variant: "destructive",
      });
    }
  };

  const handleAddMedication = async () => {
    if (!user) {
      toast({
        title: "Error",
        description: "Please log in to add medications",
        variant: "destructive",
      })
      return
    }

    if (!newMedication.name.trim()) {
      toast({
        title: "Error",
        description: "Please enter medication name",
        variant: "destructive",
      })
      return
    }

    if (!newMedication.dosage.trim()) {
      toast({
        title: "Error",
        description: "Please enter dosage",
        variant: "destructive",
      })
      return
    }

    if (!newMedication.frequency) {
      toast({
        title: "Error",
        description: "Please select frequency",
        variant: "destructive",
      })
      return
    }

    if (!newMedication.times.trim()) {
      toast({
        title: "Error",
        description: "Please enter reminder times",
        variant: "destructive",
      })
      return
    }

    if (!newMedication.stock || Number.parseInt(newMedication.stock) <= 0) {
      toast({
        title: "Error",
        description: "Please enter valid stock count",
        variant: "destructive",
      })
      return
    }

    try {
      const timesArray = newMedication.times
        .split(",")
        .map((time) => time.trim())
        .filter((time) => time.length > 0)

      if (timesArray.length === 0) {
        toast({
          title: "Error",
          description: "Please enter at least one reminder time",
          variant: "destructive",
        })
        return
      }

      const reminderData = {
        userId: user.uid,
        name: newMedication.name.trim(),
        dosage: newMedication.dosage.trim(),
        frequency: newMedication.frequency,
        times: timesArray,
        stock: Number.parseInt(newMedication.stock),
        notes: newMedication.notes.trim(),
        caregiverNotify: newMedication.caregiverNotify,
      }

      await notificationService.addPillReminder(reminderData)

      toast({
        title: "Success",
        description: "Medication added successfully",
      })

      setNewMedication({
        name: "",
        dosage: "",
        frequency: "",
        times: "",
        stock: "",
        notes: "",
        caregiverNotify: false,
      })

      setIsAddingMedication(false)

      toast({
        title: "Success!",
        description: `${newMedication.name} has been added to your medication list`,
      })
    } catch (error) {
      console.error("Error adding medication:", error)
      toast({
        title: "Error",
        description: "Failed to add medication. Please try again.",
        variant: "destructive",
      })
    }
  }

  const handleDeleteMedication = async (id: string) => {
    try {
      await notificationService.deletePillReminder(id)
      toast({
        title: "Medication Removed",
        description: "Medication has been removed from your list",
      })
    } catch (error) {
      console.error('Error deleting medication:', error)
      toast({
        title: "Error",
        description: "Failed to delete medication",
        variant: "destructive",
      })
    }
  }

  const handleMarkTaken = (id: string) => {
    setMedications(medications.map((med) => (med.id === id ? { ...med, taken: !med.taken } : med)))
  }

  const totalMedications = medications.length
  const averageAdherence =
    medications.length > 0
      ? Math.round(medications.reduce((sum, med) => sum + med.adherence, 0) / medications.length)
      : 0
  const todaysTaken = medications.filter((med) => med.taken).length
  const todaysTotal = medications.reduce((sum, med) => sum + med.times.length, 0)
  const lowStockCount = medications.filter((med) => med.stock <= 10).length

  return (
    <div className="min-h-screen bg-background">
      <HealthDashboardNav />

      <div className="lg:pl-64">
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-foreground font-sans">Pill Reminders</h1>
              <p className="text-muted-foreground font-serif">Manage your medications and track adherence</p>
            </div>
            <Dialog open={isAddingMedication} onOpenChange={setIsAddingMedication}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  Add Medication
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-md">
                <DialogHeader>
                  <DialogTitle className="font-sans">Add New Medication</DialogTitle>
                  <DialogDescription className="font-serif">
                    Enter your medication details and reminder schedule
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="med-name">Medication Name *</Label>
                    <Input
                      id="med-name"
                      placeholder="e.g., Metformin"
                      value={newMedication.name}
                      onChange={(e) => setNewMedication({ ...newMedication, name: e.target.value })}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="dosage">Dosage *</Label>
                      <Input
                        id="dosage"
                        placeholder="e.g., 500mg"
                        value={newMedication.dosage}
                        onChange={(e) => setNewMedication({ ...newMedication, dosage: e.target.value })}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="stock">Stock Count *</Label>
                      <Input
                        id="stock"
                        type="number"
                        placeholder="30"
                        value={newMedication.stock}
                        onChange={(e) => setNewMedication({ ...newMedication, stock: e.target.value })}
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="frequency">Frequency *</Label>
                    <Select
                      value={newMedication.frequency}
                      onValueChange={(value) => setNewMedication({ ...newMedication, frequency: value })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select frequency" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Once daily">Once daily</SelectItem>
                        <SelectItem value="Twice daily">Twice daily</SelectItem>
                        <SelectItem value="Three times daily">Three times daily</SelectItem>
                        <SelectItem value="Custom schedule">Custom schedule</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="times">Reminder Times * (comma separated)</Label>
                    <Input
                      id="times"
                      placeholder="e.g., 8:00 AM, 8:00 PM"
                      value={newMedication.times}
                      onChange={(e) => setNewMedication({ ...newMedication, times: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="notes">Notes (Optional)</Label>
                    <Textarea
                      id="notes"
                      placeholder="Take with food, etc."
                      value={newMedication.notes}
                      onChange={(e) => setNewMedication({ ...newMedication, notes: e.target.value })}
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="caregiver"
                      checked={newMedication.caregiverNotify}
                      onCheckedChange={(checked) => setNewMedication({ ...newMedication, caregiverNotify: checked })}
                    />
                    <Label htmlFor="caregiver" className="font-serif">
                      Notify caregiver
                    </Label>
                  </div>
                  <div className="flex gap-2">
                    <Button className="flex-1" onClick={handleAddMedication} type="button">
                      Add Medication
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => {
                        setNewMedication({
                          name: "",
                          dosage: "",
                          frequency: "",
                          times: "",
                          stock: "",
                          notes: "",
                          caregiverNotify: false,
                        })
                        setIsAddingMedication(false)
                      }}
                      type="button"
                    >
                      Cancel
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Overall Adherence</CardTitle>
                <TrendingUp className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">{averageAdherence}%</div>
                <p className="text-xs text-muted-foreground font-serif">
                  {totalMedications > 0 ? "Based on current medications" : "No medications added yet"}
                </p>
                <Progress value={averageAdherence} className="mt-2" />
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Active Medications</CardTitle>
                <Pill className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">{totalMedications}</div>
                <p className="text-xs text-muted-foreground font-serif">Currently prescribed</p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Today's Doses</CardTitle>
                <Clock className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">
                  {todaysTaken}/{todaysTotal}
                </div>
                <p className="text-xs text-muted-foreground font-serif">Taken so far</p>
                <Progress value={todaysTotal > 0 ? (todaysTaken / todaysTotal) * 100 : 0} className="mt-2" />
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Low Stock Alert</CardTitle>
                <Package className="h-4 w-4 text-destructive" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-destructive">{lowStockCount}</div>
                <p className="text-xs text-muted-foreground font-serif">Needs refill soon</p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <Tabs defaultValue="medications" className="space-y-6">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="medications">My Medications</TabsTrigger>
              <TabsTrigger value="calendar">Calendar View</TabsTrigger>
              <TabsTrigger value="adherence">Adherence Report</TabsTrigger>
            </TabsList>

            <TabsContent value="medications" className="space-y-6">
              {medications.length === 0 ? (
                <Card className="shadow-lg">
                  <CardContent className="flex flex-col items-center justify-center py-16">
                    <Pill className="w-16 h-16 text-muted-foreground mb-4" />
                    <h3 className="text-xl font-semibold font-sans mb-2">No Medications Added</h3>
                    <p className="text-muted-foreground font-serif text-center mb-6 max-w-md">
                      Start by adding your first medication to track your pill schedule and adherence.
                    </p>
                    <Button onClick={() => setIsAddingMedication(true)}>
                      <Plus className="w-4 h-4 mr-2" />
                      Add Your First Medication
                    </Button>
                  </CardContent>
                </Card>
              ) : (
                <div className="grid gap-6">
                  {medications.map((med) => (
                    <Card key={med.id} className="shadow-lg">
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className={`w-12 h-12 ${med.color} rounded-lg flex items-center justify-center`}>
                              <Pill className="w-6 h-6 text-white" />
                            </div>
                            <div>
                              <CardTitle className="font-sans">{med.name}</CardTitle>
                              <CardDescription className="font-serif">
                                {med.dosage} • {med.frequency}
                              </CardDescription>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Button
                              variant={med.taken ? "default" : "outline"}
                              size="sm"
                              onClick={() => med.id && handleMarkTaken(med.id)}
                            >
                              {med.taken ? (
                                <CheckCircle className="w-4 h-4 mr-1" />
                              ) : (
                                <Clock className="w-4 h-4 mr-1" />
                              )}
                              {med.taken ? "Taken" : "Mark Taken"}
                            </Button>
                            <Button variant="ghost" size="icon">
                              <Edit className="w-4 h-4" />
                            </Button>
                                                          <Button variant="ghost" size="icon" onClick={() => med.id && handleDeleteMedication(med.id)}>
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="grid md:grid-cols-4 gap-4">
                          <div>
                            <p className="text-sm font-medium font-sans mb-1">Next Dose</p>
                            <p className="text-sm text-muted-foreground font-serif">{med.nextDose}</p>
                          </div>
                          <div>
                            <p className="text-sm font-medium font-sans mb-1">Stock Remaining</p>
                            <div className="flex items-center gap-2">
                              <p className="text-sm text-muted-foreground font-serif">{med.stock} pills</p>
                              {med.stock <= 10 && (
                                <Badge variant="destructive" className="text-xs">
                                  Low Stock
                                </Badge>
                              )}
                            </div>
                          </div>
                          <div>
                            <p className="text-sm font-medium font-sans mb-1">Adherence</p>
                            <div className="flex items-center gap-2">
                              <Progress value={med.adherence} className="flex-1" />
                              <span className="text-sm text-muted-foreground font-serif">{med.adherence}%</span>
                            </div>
                          </div>
                          <div>
                            <p className="text-sm font-medium font-sans mb-1">Today's Status</p>
                            <div className="flex items-center gap-2">
                              {med.taken ? (
                                <CheckCircle className="w-4 h-4 text-primary" />
                              ) : (
                                <AlertCircle className="w-4 h-4 text-destructive" />
                              )}
                              <span className="text-sm text-muted-foreground font-serif">
                                {med.taken ? "Taken" : "Pending"}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="mt-4 flex flex-wrap gap-2">
                          {med.times.map((time, index) => (
                            <Badge key={index} variant="outline" className="font-serif">
                              {time}
                            </Badge>
                          ))}
                        </div>
                        {med.notes && (
                          <div className="mt-4 p-3 bg-muted/30 rounded-lg">
                            <p className="text-sm text-muted-foreground font-serif">{med.notes}</p>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            <TabsContent value="calendar" className="space-y-6">
              <div className="grid lg:grid-cols-3 gap-6">
                <Card className="lg:col-span-1 shadow-lg">
                  <CardHeader>
                    <CardTitle className="font-sans">Select Date</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Calendar
                      mode="single"
                      selected={selectedDate}
                      onSelect={setSelectedDate}
                      className="rounded-md border"
                    />
                  </CardContent>
                </Card>

                <Card className="lg:col-span-2 shadow-lg">
                  <CardHeader>
                    <CardTitle className="font-sans">Schedule for {selectedDate?.toLocaleDateString()}</CardTitle>
                    <CardDescription className="font-serif">
                      Your medication schedule for the selected date
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center gap-4 p-4 bg-muted/30 rounded-lg">
                        <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                          <Clock className="w-5 h-5 text-primary" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium font-sans">8:00 AM - Metformin 500mg</p>
                          <p className="text-sm text-muted-foreground font-serif">Take with breakfast</p>
                        </div>
                        <CheckCircle className="w-5 h-5 text-primary" />
                      </div>

                      <div className="flex items-center gap-4 p-4 bg-muted/30 rounded-lg">
                        <div className="w-10 h-10 bg-secondary/10 rounded-full flex items-center justify-center">
                          <Clock className="w-5 h-5 text-secondary" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium font-sans">9:00 AM - Lisinopril 10mg</p>
                          <p className="text-sm text-muted-foreground font-serif">Blood pressure medication</p>
                        </div>
                        <CheckCircle className="w-5 h-5 text-primary" />
                      </div>

                      <div className="flex items-center gap-4 p-4 bg-muted/30 rounded-lg">
                        <div className="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center">
                          <Clock className="w-5 h-5 text-accent" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium font-sans">8:00 PM - Metformin 500mg</p>
                          <p className="text-sm text-muted-foreground font-serif">Take with dinner</p>
                        </div>
                        <AlertCircle className="w-5 h-5 text-muted-foreground" />
                      </div>

                      <div className="flex items-center gap-4 p-4 bg-muted/30 rounded-lg">
                        <div className="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center">
                          <Clock className="w-5 h-5 text-accent" />
                        </div>
                        <div className="flex-1">
                          <p className="font-medium font-sans">10:00 PM - Atorvastatin 20mg</p>
                          <p className="text-sm text-muted-foreground font-serif">Cholesterol medication</p>
                        </div>
                        <AlertCircle className="w-5 h-5 text-muted-foreground" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="adherence" className="space-y-6">
              <div className="grid lg:grid-cols-2 gap-6">
                <Card className="shadow-lg">
                  <CardHeader>
                    <CardTitle className="font-sans">Weekly Adherence</CardTitle>
                    <CardDescription className="font-serif">
                      Your medication adherence over the past week
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day, index) => {
                        const adherence = [100, 75, 100, 100, 50, 100, 100][index]
                        return (
                          <div key={day} className="flex items-center gap-4">
                            <span className="w-12 text-sm font-medium font-sans">{day}</span>
                            <Progress value={adherence} className="flex-1" />
                            <span className="w-12 text-sm text-muted-foreground font-serif">{adherence}%</span>
                          </div>
                        )
                      })}
                    </div>
                  </CardContent>
                </Card>

                <Card className="shadow-lg">
                  <CardHeader>
                    <CardTitle className="font-sans">Medication Performance</CardTitle>
                    <CardDescription className="font-serif">Individual medication adherence rates</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {medications.map((med) => (
                        <div key={med.id} className="flex items-center gap-4">
                          <div className={`w-8 h-8 ${med.color} rounded-lg flex items-center justify-center`}>
                            <Pill className="w-4 h-4 text-white" />
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-medium font-sans">{med.name}</p>
                            <Progress value={med.adherence} className="mt-1" />
                          </div>
                          <span className="text-sm text-muted-foreground font-serif">{med.adherence}%</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="shadow-lg">
                <CardHeader>
                  <CardTitle className="font-sans">Caregiver Notifications</CardTitle>
                  <CardDescription className="font-serif">
                    Manage who gets notified about your medication adherence
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
                      <div className="flex items-center gap-3">
                        <Users className="w-5 h-5 text-primary" />
                        <div>
                          <p className="font-medium font-sans">Dr. Sarah Patel</p>
                          <p className="text-sm text-muted-foreground font-serif">Primary Care Physician</p>
                        </div>
                      </div>
                      <Switch defaultChecked />
                    </div>
                    <div className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
                      <div className="flex items-center gap-3">
                        <Users className="w-5 h-5 text-primary" />
                        <div>
                          <p className="font-medium font-sans">John Doe Jr.</p>
                          <p className="text-sm text-muted-foreground font-serif">Family Caregiver</p>
                        </div>
                      </div>
                      <Switch defaultChecked />
                    </div>
                    <Button variant="outline" className="w-full bg-transparent">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Caregiver
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
