from django.db import models
from django.contrib import admin


# Solution-related models
class UserSolution(models.Model):
    '''
    Represents a user submitted solution of a given problem.
    '''

    user = models.ForeignKey('auth.User')
    problem = models.ForeignKey('problems.Problem')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s solution of " +
                self.problem.__unicode__())


class OrgSolution(models.Model):
    '''
    Represents an ideal solution of a problem. There can be multiple ideal
    solutions (more organizers trying to solve it, more ways of solving).
    '''
    organizer = models.ForeignKey('auth.User')
    problem = models.ForeignKey('problems.Problem')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s ideal solution of " +
                self.problem.__unicode__())


# Problem-related models
class Problem(models.Model):
    '''
    Represents a problem.
    '''

    author = models.ForeignKey('auth.User')
    text = models.CharField(max_length=1000)
    # rating = models.ForeignKey('ratings.Rating')
    category = models.ForeignKey('problems.ProblemCategory')
    competition = models.ForeignKey('competitions.Competition')

    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Fields added via foreign keys:

    #  orgsolution_set
    #  problemset_set
    #  user_set
    #  usersolution_set

    def __unicode__(self):
        return self.text


class ProblemSet(models.Model):
    '''
    Represents a collections of problems. This can (optionally) be used at
    event or competition, which organizer should mark here.
    '''

    competition = models.ForeignKey('competitions.Competition')
    leaflet = models.ForeignKey('leaflets.Leaflet',
                                blank=True, null=True)
    problems = models.ManyToManyField(Problem)

    def __unicode__(self):
        return u"ProblemSet for " + self.competition.__unicode__()


class ProblemCategory(models.Model):
    '''
    Represents a category of problems, like geometry or functional equations.
    '''

    name = models.CharField(max_length=50)

    # Fields added via foreign keys:

        # problem_set

    def __unicode__(self):
        return self.name


# Register to the admin site
admin.site.register(Problem)
admin.site.register(ProblemSet)
admin.site.register(UserSolution)
admin.site.register(OrgSolution)
admin.site.register(ProblemCategory)
