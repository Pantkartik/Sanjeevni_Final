"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Brain,
  Heart,
  Smile,
  Frown,
  Meh,
  TrendingUp,
  BookOpen,
  Headphones,
  Target,
  Award,
  Phone,
  MessageCircle,
  Play,
  RotateCcw,
} from "lucide-react"
import { HealthDashboardNav } from "@/components/health-dashboard-nav"

const moodData = [
  { date: "Mon", mood: 4, stress: 3, anxiety: 2 },
  { date: "Tue", mood: 3, stress: 4, anxiety: 3 },
  { date: "Wed", mood: 5, stress: 2, anxiety: 1 },
  { date: "Thu", mood: 4, stress: 3, anxiety: 2 },
  { date: "Fri", mood: 5, stress: 2, anxiety: 1 },
  { date: "Sat", mood: 4, stress: 3, anxiety: 2 },
  { date: "Sun", mood: 4, stress: 2, anxiety: 2 },
]

const journalEntries = [
  {
    id: 1,
    date: "2024-01-15",
    mood: 4,
    title: "Good day at work",
    content: "Had a productive meeting and felt accomplished. Stress levels were manageable.",
    sentiment: "positive",
  },
  {
    id: 2,
    date: "2024-01-14",
    mood: 3,
    title: "Feeling overwhelmed",
    content: "Too many tasks today. Need to practice breathing exercises more regularly.",
    sentiment: "neutral",
  },
  {
    id: 3,
    date: "2024-01-13",
    mood: 5,
    title: "Great weekend",
    content: "Spent time with family and felt very relaxed. Meditation session was helpful.",
    sentiment: "positive",
  },
]

const cbtExercises = [
  {
    id: 1,
    title: "Thought Record",
    description: "Identify and challenge negative thought patterns",
    duration: "10-15 min",
    category: "Cognitive",
    completed: false,
  },
  {
    id: 2,
    title: "Progressive Muscle Relaxation",
    description: "Reduce physical tension and stress",
    duration: "15-20 min",
    category: "Relaxation",
    completed: true,
  },
  {
    id: 3,
    title: "Gratitude Practice",
    description: "Focus on positive aspects of your day",
    duration: "5-10 min",
    category: "Mindfulness",
    completed: false,
  },
  {
    id: 4,
    title: "Breathing Exercise",
    description: "4-7-8 breathing technique for anxiety",
    duration: "5 min",
    category: "Breathing",
    completed: true,
  },
]

export default function MentalHealthPage() {
  const [currentMood, setCurrentMood] = useState(4)
  const [stressLevel, setStressLevel] = useState([3])
  const [anxietyLevel, setAnxietyLevel] = useState([2])
  const [isJournaling, setIsJournaling] = useState(false)
  const [journalEntry, setJournalEntry] = useState("")
  const [isBreathingActive, setIsBreathingActive] = useState(false)
  const [breathingPhase, setBreathingPhase] = useState("inhale")

  const getMoodIcon = (mood: number) => {
    if (mood >= 4) return <Smile className="w-6 h-6 text-primary" />
    if (mood >= 3) return <Meh className="w-6 h-6 text-accent" />
    return <Frown className="w-6 h-6 text-destructive" />
  }

  const getMoodColor = (mood: number) => {
    if (mood >= 4) return "text-primary"
    if (mood >= 3) return "text-accent"
    return "text-destructive"
  }

  const startBreathingExercise = () => {
    setIsBreathingActive(true)
    // Simulate breathing cycle
    const cycle = () => {
      setBreathingPhase("inhale")
      setTimeout(() => setBreathingPhase("hold"), 4000)
      setTimeout(() => setBreathingPhase("exhale"), 11000)
      setTimeout(() => setBreathingPhase("pause"), 19000)
    }
    cycle()
    const interval = setInterval(cycle, 20000)
    setTimeout(() => {
      clearInterval(interval)
      setIsBreathingActive(false)
      setBreathingPhase("inhale")
    }, 300000) // 5 minutes
  }

  return (
    <div className="min-h-screen bg-background">
      <HealthDashboardNav />

      <div className="lg:pl-64">
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-foreground font-sans">Mental Health Tracker</h1>
              <p className="text-muted-foreground font-serif">Monitor your mental wellness and practice self-care</p>
            </div>
            <Dialog open={isJournaling} onOpenChange={setIsJournaling}>
              <DialogTrigger asChild>
                <Button>
                  <BookOpen className="w-4 h-4 mr-2" />
                  New Journal Entry
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-2xl">
                <DialogHeader>
                  <DialogTitle className="font-sans">Daily Journal</DialogTitle>
                  <DialogDescription className="font-serif">
                    Reflect on your day and track your mental wellness
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-6">
                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm font-medium font-sans">How are you feeling today?</Label>
                      <div className="flex items-center gap-4 mt-2">
                        {[1, 2, 3, 4, 5].map((mood) => (
                          <button
                            key={mood}
                            onClick={() => setCurrentMood(mood)}
                            className={`p-3 rounded-lg border-2 transition-colors ${
                              currentMood === mood
                                ? "border-primary bg-primary/10"
                                : "border-border hover:border-primary/50"
                            }`}
                          >
                            {getMoodIcon(mood)}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label className="text-sm font-medium font-sans">Stress Level: {stressLevel[0]}/5</Label>
                      <Slider
                        value={stressLevel}
                        onValueChange={setStressLevel}
                        max={5}
                        min={1}
                        step={1}
                        className="w-full"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label className="text-sm font-medium font-sans">Anxiety Level: {anxietyLevel[0]}/5</Label>
                      <Slider
                        value={anxietyLevel}
                        onValueChange={setAnxietyLevel}
                        max={5}
                        min={1}
                        step={1}
                        className="w-full"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="journal-entry">What's on your mind?</Label>
                    <Textarea
                      id="journal-entry"
                      value={journalEntry}
                      onChange={(e) => setJournalEntry(e.target.value)}
                      placeholder="Write about your thoughts, feelings, or experiences today..."
                      className="min-h-32"
                    />
                  </div>

                  <div className="flex gap-2">
                    <Button className="flex-1">Save Entry</Button>
                    <Button variant="outline" onClick={() => setIsJournaling(false)}>
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
                <CardTitle className="text-sm font-medium font-sans">Current Mood</CardTitle>
                <Brain className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  {getMoodIcon(4)}
                  <span className={`text-2xl font-bold ${getMoodColor(4)}`}>Good</span>
                </div>
                <p className="text-xs text-muted-foreground font-serif">Above average today</p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Weekly Average</CardTitle>
                <TrendingUp className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">4.1</div>
                <p className="text-xs text-muted-foreground font-serif">+0.3 from last week</p>
                <Progress value={82} className="mt-2" />
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Exercises Completed</CardTitle>
                <Target className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">2/4</div>
                <p className="text-xs text-muted-foreground font-serif">Today's goal</p>
                <Progress value={50} className="mt-2" />
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium font-sans">Streak</CardTitle>
                <Award className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground">7</div>
                <p className="text-xs text-muted-foreground font-serif">Days tracking</p>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <Tabs defaultValue="today" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="today">Today</TabsTrigger>
              <TabsTrigger value="exercises">Exercises</TabsTrigger>
              <TabsTrigger value="journal">Journal</TabsTrigger>
              <TabsTrigger value="insights">Insights</TabsTrigger>
            </TabsList>

            <TabsContent value="today" className="space-y-6">
              <div className="grid lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                  {/* Mood Check-in */}
                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="font-sans">Daily Check-in</CardTitle>
                      <CardDescription className="font-serif">How are you feeling right now?</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-6">
                        <div>
                          <Label className="text-sm font-medium font-sans mb-4 block">Mood</Label>
                          <div className="flex items-center justify-between">
                            {[1, 2, 3, 4, 5].map((mood) => (
                              <button
                                key={mood}
                                onClick={() => setCurrentMood(mood)}
                                className={`p-4 rounded-lg border-2 transition-colors ${
                                  currentMood === mood
                                    ? "border-primary bg-primary/10"
                                    : "border-border hover:border-primary/50"
                                }`}
                              >
                                {getMoodIcon(mood)}
                              </button>
                            ))}
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <Label className="text-sm font-medium font-sans">Stress Level</Label>
                            <Slider value={stressLevel} onValueChange={setStressLevel} max={5} min={1} step={1} />
                            <div className="flex justify-between text-xs text-muted-foreground font-serif">
                              <span>Low</span>
                              <span>High</span>
                            </div>
                          </div>
                          <div className="space-y-2">
                            <Label className="text-sm font-medium font-sans">Anxiety Level</Label>
                            <Slider value={anxietyLevel} onValueChange={setAnxietyLevel} max={5} min={1} step={1} />
                            <div className="flex justify-between text-xs text-muted-foreground font-serif">
                              <span>Low</span>
                              <span>High</span>
                            </div>
                          </div>
                        </div>

                        <Button className="w-full">Save Check-in</Button>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Weekly Mood Trend */}
                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="font-sans">Weekly Mood Trend</CardTitle>
                      <CardDescription className="font-serif">
                        Your emotional wellness over the past week
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {moodData.map((day) => (
                          <div key={day.date} className="flex items-center gap-4">
                            <span className="w-12 text-sm font-medium font-sans">{day.date}</span>
                            <div className="flex-1 space-y-2">
                              <div className="flex items-center gap-2">
                                <span className="text-xs text-muted-foreground font-serif w-12">Mood</span>
                                <Progress value={day.mood * 20} className="flex-1" />
                                <span className="text-xs text-muted-foreground font-serif w-8">{day.mood}/5</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className="text-xs text-muted-foreground font-serif w-12">Stress</span>
                                <Progress value={day.stress * 20} className="flex-1" />
                                <span className="text-xs text-muted-foreground font-serif w-8">{day.stress}/5</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Right Column */}
                <div className="space-y-6">
                  {/* Quick Actions */}
                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="font-sans">Quick Relief</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <Button
                        className="w-full justify-start bg-transparent"
                        variant="outline"
                        onClick={startBreathingExercise}
                      >
                        <Headphones className="w-4 h-4 mr-2" />
                        Breathing Exercise
                      </Button>
                      <Button className="w-full justify-start bg-transparent" variant="outline">
                        <Heart className="w-4 h-4 mr-2" />
                        Gratitude Practice
                      </Button>
                      <Button className="w-full justify-start bg-transparent" variant="outline">
                        <Brain className="w-4 h-4 mr-2" />
                        Mindfulness
                      </Button>
                      <Button className="w-full justify-start bg-transparent" variant="outline">
                        <BookOpen className="w-4 h-4 mr-2" />
                        Thought Record
                      </Button>
                    </CardContent>
                  </Card>

                  {/* Crisis Support */}
                  <Card className="shadow-lg border-destructive/20">
                    <CardHeader>
                      <CardTitle className="font-sans text-destructive">Need Immediate Help?</CardTitle>
                      <CardDescription className="font-serif">Crisis support resources</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <Button variant="destructive" className="w-full">
                        <Phone className="w-4 h-4 mr-2" />
                        Crisis Hotline
                      </Button>
                      <Button variant="outline" className="w-full bg-transparent">
                        <MessageCircle className="w-4 h-4 mr-2" />
                        Chat Support
                      </Button>
                      <p className="text-xs text-muted-foreground font-serif">
                        Available 24/7 for immediate mental health support
                      </p>
                    </CardContent>
                  </Card>

                  {/* Breathing Exercise Modal */}
                  {isBreathingActive && (
                    <Card className="shadow-lg border-primary/20">
                      <CardHeader>
                        <CardTitle className="font-sans">4-7-8 Breathing</CardTitle>
                      </CardHeader>
                      <CardContent className="text-center space-y-4">
                        <div className="w-24 h-24 mx-auto rounded-full border-4 border-primary flex items-center justify-center">
                          <span className="text-lg font-bold text-primary capitalize">{breathingPhase}</span>
                        </div>
                        <div className="space-y-2">
                          <p className="text-sm font-medium font-sans capitalize">{breathingPhase}</p>
                          <p className="text-xs text-muted-foreground font-serif">
                            {breathingPhase === "inhale" && "Breathe in for 4 seconds"}
                            {breathingPhase === "hold" && "Hold for 7 seconds"}
                            {breathingPhase === "exhale" && "Exhale for 8 seconds"}
                            {breathingPhase === "pause" && "Pause briefly"}
                          </p>
                        </div>
                        <Button variant="outline" onClick={() => setIsBreathingActive(false)}>
                          Stop Exercise
                        </Button>
                      </CardContent>
                    </Card>
                  )}
                </div>
              </div>
            </TabsContent>

            <TabsContent value="exercises" className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {cbtExercises.map((exercise) => (
                  <Card key={exercise.id} className="shadow-lg">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div>
                          <CardTitle className="font-sans">{exercise.title}</CardTitle>
                          <CardDescription className="font-serif">{exercise.description}</CardDescription>
                        </div>
                        {exercise.completed && <Award className="w-5 h-5 text-primary" />}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <Badge variant="outline">{exercise.category}</Badge>
                          <span className="text-sm text-muted-foreground font-serif">{exercise.duration}</span>
                        </div>
                        <Button className="w-full" variant={exercise.completed ? "outline" : "default"}>
                          {exercise.completed ? (
                            <>
                              <RotateCcw className="w-4 h-4 mr-2" />
                              Repeat Exercise
                            </>
                          ) : (
                            <>
                              <Play className="w-4 h-4 mr-2" />
                              Start Exercise
                            </>
                          )}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="journal" className="space-y-6">
              <div className="space-y-6">
                {journalEntries.map((entry) => (
                  <Card key={entry.id} className="shadow-lg">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          {getMoodIcon(entry.mood)}
                          <div>
                            <CardTitle className="font-sans">{entry.title}</CardTitle>
                            <CardDescription className="font-serif">
                              {new Date(entry.date).toLocaleDateString()}
                            </CardDescription>
                          </div>
                        </div>
                        <Badge variant={entry.sentiment === "positive" ? "default" : "secondary"}>
                          {entry.sentiment}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground font-serif">{entry.content}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="insights" className="space-y-6">
              <div className="grid lg:grid-cols-2 gap-6">
                <Card className="shadow-lg">
                  <CardHeader>
                    <CardTitle className="font-sans">Mental Health Insights</CardTitle>
                    <CardDescription className="font-serif">
                      AI-powered analysis of your mental wellness
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="p-4 bg-primary/5 rounded-lg border border-primary/20">
                        <p className="text-sm font-medium font-sans mb-2">Positive Trend</p>
                        <p className="text-xs text-muted-foreground font-serif">
                          Your mood has been consistently improving over the past week. Keep up the great work with your
                          daily exercises!
                        </p>
                      </div>
                      <div className="p-4 bg-accent/5 rounded-lg border border-accent/20">
                        <p className="text-sm font-medium font-sans mb-2">Recommendation</p>
                        <p className="text-xs text-muted-foreground font-serif">
                          Consider practicing breathing exercises during high-stress periods. Your data shows they're
                          most effective for you.
                        </p>
                      </div>
                      <div className="p-4 bg-muted/30 rounded-lg">
                        <p className="text-sm font-medium font-sans mb-2">Pattern Recognition</p>
                        <p className="text-xs text-muted-foreground font-serif">
                          Your mood tends to be highest on weekends and after completing mindfulness exercises.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="shadow-lg">
                  <CardHeader>
                    <CardTitle className="font-sans">Wellness Goals</CardTitle>
                    <CardDescription className="font-serif">Track your mental health objectives</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium font-sans">Daily Check-ins</span>
                          <span className="text-sm text-muted-foreground font-serif">7/7</span>
                        </div>
                        <Progress value={100} />
                      </div>
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium font-sans">Weekly Exercises</span>
                          <span className="text-sm text-muted-foreground font-serif">5/7</span>
                        </div>
                        <Progress value={71} />
                      </div>
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium font-sans">Journal Entries</span>
                          <span className="text-sm text-muted-foreground font-serif">3/5</span>
                        </div>
                        <Progress value={60} />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
