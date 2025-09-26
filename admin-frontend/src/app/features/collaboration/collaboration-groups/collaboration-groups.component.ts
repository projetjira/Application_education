import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CollaborationService } from '../../../core/services/collaboration.service';
import { CollaborationGroup } from '../../../core/models/collaboration';
import { CreateGroupDialogComponent } from '../create-group-dialog/create-group-dialog.component';

@Component({
  selector: 'app-collaboration-groups',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule, MatButtonModule, MatIconModule],
  template: `
    <div class="groups-container">
      <div class="header">
        <h2>Collaboration Groups</h2>
        <button mat-raised-button color="primary" (click)="openCreateGroupDialog()">
          <mat-icon>add</mat-icon>
          Create Group
        </button>
      </div>

      <div class="groups-grid" *ngIf="groups.length > 0">
        <mat-card *ngFor="let group of groups" class="group-card">
          <mat-card-header>
            <mat-card-title>{{ group.name }}</mat-card-title>
            <mat-card-subtitle>
              Created by {{ group.creator_name }} • 
              {{ group.member_count }} member{{group.member_count !== 1 ? 's' : ''}}
            </mat-card-subtitle>
          </mat-card-header>
          
          <mat-card-content>
            <p *ngIf="group.description">{{ group.description }}</p>
            <p class="created-date">Created: {{ formatDate(group.created_at) }}</p>
          </mat-card-content>
          
          <mat-card-actions>
            <button mat-button color="primary" [routerLink]="['/collaboration/groups', group.group_id]">
              <mat-icon>visibility</mat-icon>
              View
            </button>
            <button mat-button color="accent" [routerLink]="['/collaboration/groups', group.group_id, 'discussions']">
              <mat-icon>forum</mat-icon>
              Discussions
            </button>
          </mat-card-actions>
        </mat-card>
      </div>

      <div class="empty-state" *ngIf="groups.length === 0 && !loading">
        <mat-icon class="empty-icon">groups</mat-icon>
        <h3>No collaboration groups yet</h3>
        <p>Create your first group to start collaborating with students.</p>
        <button mat-raised-button color="primary" (click)="openCreateGroupDialog()">
          Create First Group
        </button>
      </div>

      <div class="loading" *ngIf="loading">
        <p>Loading groups...</p>
      </div>
    </div>
  `,
  styles: [`
    .groups-container {
      padding: 20px;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .groups-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }

    .group-card {
      height: fit-content;
    }

    .created-date {
      font-size: 0.9em;
      color: #666;
      margin-top: 10px;
    }

    .empty-state {
      text-align: center;
      padding: 40px;
      color: #666;
    }

    .empty-icon {
      font-size: 48px;
      margin-bottom: 16px;
      color: #ccc;
    }

    .loading {
      text-align: center;
      padding: 20px;
    }
  `]
})
export class CollaborationGroupsComponent implements OnInit {
  groups: CollaborationGroup[] = [];
  loading = false;

  constructor(
    private collaborationService: CollaborationService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadGroups();
  }

  loadGroups(): void {
    this.loading = true;
    this.collaborationService.getGroups().subscribe({
      next: (response) => {
        this.groups = response.groups;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading groups:', error);
        this.snackBar.open('Error loading groups', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  openCreateGroupDialog(): void {
    const dialogRef = this.dialog.open(CreateGroupDialogComponent, {
      width: '500px'
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadGroups(); // Refresh the list
      }
    });
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
}