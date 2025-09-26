import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CollaborationService } from '../../../core/services/collaboration.service';

@Component({
  selector: 'app-create-group-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ],
  template: `
    <h2 mat-dialog-title>Create Collaboration Group</h2>
    
    <form [formGroup]="groupForm" (ngSubmit)="onSubmit()">
      <div mat-dialog-content>
        <mat-form-field appearance="fill" class="full-width">
          <mat-label>Group Name</mat-label>
          <input matInput formControlName="name" placeholder="Enter group name" required>
          <mat-error *ngIf="groupForm.get('name')?.hasError('required')">
            Group name is required
          </mat-error>
        </mat-form-field>

        <mat-form-field appearance="fill" class="full-width">
          <mat-label>Description (optional)</mat-label>
          <textarea matInput formControlName="description" rows="3" 
                    placeholder="Describe the purpose of this group"></textarea>
        </mat-form-field>
      </div>

      <div mat-dialog-actions>
        <button mat-button type="button" (click)="onCancel()">Cancel</button>
        <button mat-raised-button color="primary" type="submit" 
                [disabled]="groupForm.invalid || isSubmitting">
          {{ isSubmitting ? 'Creating...' : 'Create Group' }}
        </button>
      </div>
    </form>
  `,
  styles: [`
    .full-width {
      width: 100%;
      margin-bottom: 15px;
    }
    
    mat-dialog-content {
      min-width: 400px;
    }
  `]
})
export class CreateGroupDialogComponent {
  groupForm: FormGroup;
  isSubmitting = false;

  constructor(
    private fb: FormBuilder,
    private collaborationService: CollaborationService,
    private dialogRef: MatDialogRef<CreateGroupDialogComponent>,
    private snackBar: MatSnackBar
  ) {
    this.groupForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      description: ['', Validators.maxLength(500)]
    });
  }

  onSubmit(): void {
    if (this.groupForm.valid && !this.isSubmitting) {
      this.isSubmitting = true;
      
      // For now, using a dummy admin ID (1). In a real app, this would come from auth service
      const createdBy = 1;
      
      this.collaborationService.createGroup(this.groupForm.value, createdBy).subscribe({
        next: (response) => {
          this.snackBar.open('Group created successfully!', 'Close', { duration: 3000 });
          this.dialogRef.close(true);
        },
        error: (error) => {
          console.error('Error creating group:', error);
          this.snackBar.open('Error creating group. Please try again.', 'Close', { duration: 3000 });
          this.isSubmitting = false;
        }
      });
    }
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}